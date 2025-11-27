import csv
import json
import os
import sys
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.align import Align
    from rich.prompt import Prompt
    from rich import box
except ImportError:
    print("❌ Biblioteca 'rich' não encontrada. Rode: pip install rich")
    sys.exit()

# --- CONFIGURAÇÕES ---
ARQUIVO_JSON = "carteira.json"
console = Console()

# --- UTILITÁRIOS VISUAIS ---

def limpar_tela():
    console.clear()

def cabecalho(titulo):
    texto = f"[bold cyan]{titulo}[/]"
    console.print(Panel(Align.center(texto), border_style="blue"))

def carregar_carteira():
    if not os.path.exists(ARQUIVO_JSON): return []
    try:
        with open(ARQUIVO_JSON, "r") as f: return json.load(f)
    except: return []

def salvar_carteira(dados):
    dados.sort(key=lambda x: x['data'])
    with open(ARQUIVO_JSON, "w") as f: json.dump(dados, f, indent=4)

# --- LÓGICA DE LIMPEZA ---

def limpar_numero(texto):
    """Limpa moedas (BTC, BRL, R$) e converte para float"""
    sujeira = ['BTC', 'BRL', 'USD', 'USDT', 'ETH', 'LTC', ' ', 'R$']
    texto_limpo = texto.upper()
    for s in sujeira:
        texto_limpo = texto_limpo.replace(s, '')
    try:
        return float(texto_limpo)
    except: return 0.0

def limpar_data(texto):
    """Tenta converter vários formatos de data para ISO"""
    data_pura = texto.strip().split(' ')[0] # Remove hora
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
    for fmt in formatos:
        try:
            dt = datetime.strptime(data_pura, fmt)
            return dt.strftime("%Y-%m-%d")
        except: continue
    return None

def detectar_arquivo_csv():
    """Lista CSVs bonitinhos e ignora o da Selic"""
    # Filtra CSVs e ignora 'selic.csv'
    arquivos = [f for f in os.listdir('.') if f.lower().endswith('.csv') and 'selic' not in f.lower()]
    
    if not arquivos:
        return None
    
    if len(arquivos) == 1:
        return arquivos[0]
    
    # Se tiver mais de um, mostra tabela de escolha
    console.print("\n[yellow]Encontrei múltiplos arquivos. Qual deles?[/]")
    
    table = Table(box=box.SIMPLE)
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Nome do Arquivo", style="bold white")
    
    for i, arq in enumerate(arquivos):
        table.add_row(str(i+1), arq)
        
    console.print(table)
    
    try:
        escolha = int(Prompt.ask("Digite o número")) - 1
        if 0 <= escolha < len(arquivos):
            return arquivos[escolha]
    except: pass
    
    return None

# --- MOTOR PRINCIPAL ---

def importar_csv():
    limpar_tela()
    cabecalho("IMPORTADOR DE EXTRATO (CSV)")
    
    arquivo_alvo = detectar_arquivo_csv()
    
    if not arquivo_alvo:
        console.print(Panel("❌ Nenhum extrato CSV encontrado.\n\nBaixe da corretora e coloque nesta pasta.", border_style="red"))
        return

    console.print(f"📂 Lendo: [bold yellow]{arquivo_alvo}[/]...")
    
    linhas = []
    try:
        with open(arquivo_alvo, 'r', encoding='utf-8') as f:
            sample = f.read(1024)
            dialect = csv.Sniffer().sniff(sample)
            f.seek(0)
            leitor = csv.reader(f, dialect)
            linhas = list(leitor)
    except Exception as e:
        console.print(f"[red]Erro ao ler arquivo: {e}[/]")
        return

    if not linhas:
        console.print("[red]Arquivo vazio.[/]"); return

    cabecalho_csv = linhas[0]
    
    # --- MAPEAMENTO DE COLUNAS (TABELA BONITA) ---
    console.print("\n[bold]Mapeamento de Colunas:[/]")
    
    grid_cols = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    grid_cols.add_column("Índice", justify="center", style="cyan")
    grid_cols.add_column("Nome da Coluna no CSV")
    
    for i, col in enumerate(cabecalho_csv):
        grid_cols.add_row(str(i), col)
        
    console.print(grid_cols)
    
    console.print(Panel("Digite os números das colunas correspondentes separados por ESPAÇO.\nExemplo: [cyan]0 2 4[/]", border_style="dim"))
    
    entrada = Prompt.ask("[bold yellow]> [DATA] [SATS] [VALOR GASTO][/]").strip()
    
    try:
        partes = entrada.split()
        idx_data = int(partes[0])
        idx_sats = int(partes[1])
        idx_custo = int(partes[2])
    except:
        console.print("[red]❌ Entrada inválida. Precisa ser 3 números.[/]"); return

    # --- PROCESSAMENTO COM SPINNER ---
    novos = 0
    duplicados = 0
    erros = 0
    
    carteira = carregar_carteira()
    
    with console.status("[bold green]Importando e processando transações...[/]") as status:
        for i, linha in enumerate(linhas[1:], start=2):
            if len(linha) <= max(idx_data, idx_sats, idx_custo): 
                continue 
                
            raw_data = linha[idx_data]
            raw_sats = linha[idx_sats]
            raw_custo = linha[idx_custo]

            # Tratamento
            data_iso = limpar_data(raw_data)
            if not data_iso:
                erros += 1; continue
                
            qtd_float = limpar_numero(raw_sats)
            custo_float = limpar_numero(raw_custo)
            sats = int(qtd_float * 100_000_000)
            
            if sats <= 0 or custo_float <= 0: continue

            # Checa Duplicata
            ja_existe = False
            for item in carteira:
                if (item['data'] == data_iso and 
                    abs(item['sats'] - sats) < 5 and 
                    abs(item['custo'] - custo_float) < 0.05):
                    ja_existe = True
                    break
            
            if ja_existe:
                duplicados += 1
            else:
                # Cria novo registro
                btc_fracao = sats / 100_000_000
                p_hist = custo_float / btc_fracao if btc_fracao > 0 else 0
                
                carteira.append({
                    "data": data_iso,
                    "sats": sats,
                    "custo": custo_float,
                    "preco_historico": p_hist
                })
                novos += 1

    # --- RELATÓRIO FINAL ---
    if novos > 0:
        salvar_carteira(carteira)
        
    tabela_res = Table.grid(padding=(0, 2))
    tabela_res.add_column(style="white")
    tabela_res.add_column(justify="right", style="bold")
    
    tabela_res.add_row("Novos Registros:", f"[green]{novos}[/]")
    tabela_res.add_row("Duplicados (Ignorados):", f"[yellow]{duplicados}[/]")
    tabela_res.add_row("Erros de Leitura:", f"[red]{erros}[/]")
    
    estilo_borda = "green" if novos > 0 else "yellow"
    titulo_painel = "✅ Importação Concluída" if novos > 0 else "⚠️ Nenhuma novidade"
    
    console.print("\n")
    console.print(Panel(
        Align.center(tabela_res),
        title=titulo_painel,
        border_style=estilo_borda,
        padding=(1, 2)
    ))
    
    console.input("\n[dim]Pressione Enter para sair...[/]")

if __name__ == "__main__":
    importar_csv()
