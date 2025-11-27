​📥 Importador Universal de Extratos Cripto
​Bem-vindo ao Importador Universal! Esta é uma ferramenta desenvolvida em Python para facilitar a vida de investidores de criptomoedas.
​Se você faz compras recorrentes em corretoras (como Binance, Mercado Bitcoin, Foxbit, etc.), sabe que é chato ficar anotando cada compra manualmente. Este programa lê o arquivo .CSV (o extrato) que a corretora gera e cria automaticamente o banco de dados organizado para você.
​🚀 O que este programa faz?
​Lê qualquer CSV: Não importa a corretora, desde que tenha colunas de Data, Quantidade e Valor.
​Limpeza Inteligente: Ele remove textos "sujos" como "BTC", "BRL", "R$", deixando apenas os números puros.
​Evita Duplicatas: Se você tentar importar o mesmo arquivo duas vezes, ele detecta e não salva as compras repetidas.
​Interface Visual: Usa cores e tabelas bonitas no terminal para facilitar o uso.
​Gera o Banco de Dados: Cria/Atualiza um arquivo carteira.json que serve de memória para outros programas de portfólio.
​🛠️ Pré-requisitos (O que você precisa ter)
​Antes de começar, você precisa ter duas coisas instaladas no seu computador ou celular (Termux):
​1. Python (A linguagem do programa)
​Se você ainda não tem, baixe e instale:
​Windows: Baixar Python no site oficial. (Dica: Na instalação, marque a caixinha "Add Python to PATH").
​Android (Termux): Digite pkg install python.
​2. Biblioteca Visual (Rich)
​Este programa usa uma biblioteca especial para deixar as tabelas coloridas e bonitas.
Abra seu terminal (CMD, PowerShell ou Termux) e digite:

'''bash
pip install rich
'''

📂 Como Usar (Passo a Passo)
​Passo 1: Baixe o Extrato da sua Corretora
​Vá no site ou app da sua corretora (ex: Binance) e procure por "Histórico de Transações", "Extrato" ou "Trade History". Baixe o arquivo no formato .CSV.
​Passo 2: Coloque na Pasta
​Pegue esse arquivo .csv que você baixou e coloque na mesma pasta onde está este programa (importador_visual.py).
​Dica: Não precisa renomear o arquivo, o programa vai encontrá-lo.
​Passo 3: Rode o Programa
​Abra o terminal na pasta do projeto e execute:

'''bash
python importador_visual.py

'''

Passo 4: Mapeando as Colunas (A Mágica)
​Como cada corretora organiza o arquivo de um jeito diferente, o programa vai te mostrar uma lista numerada das colunas e pedir ajuda uma única vez.
​Exemplo do que vai aparecer na tela:
''' bash
[0] Date(UTC)
[1] OrderNo
[2] Pair
[3] Type
[4] Amount (BTC)
[5] Total (BRL)

'''

O programa vai perguntar: "Digite os números das colunas [DATA] [SATS] [VALOR GASTO]".
​Olhando o exemplo acima:
​A Data é a coluna 0.
​A Quantidade (Amount) é a coluna 4.
​O Valor Gasto (Total) é a coluna 5.
​Você só precisa digitar:
0 4 5
(e apertar Enter).
​Pronto! 🎉
​O programa vai processar tudo, ignorar o que já foi salvo e mostrar um relatório verde de sucesso:
​"✅ SUCESSO! 15 compras importadas."
​💾 Onde ficam meus dados?
​O programa vai criar (ou atualizar) automaticamente um arquivo chamado carteira.json na mesma pasta.
​Não apague esse arquivo! Ele é a memória do seu portfólio.
​Se você quiser zerar tudo e começar de novo, basta apagar o carteira.json.
​❓ Perguntas Frequentes
​P: O arquivo da minha corretora tem hora junto com a data (ex: 2023-10-25 14:30). Funciona?
R: Sim! O programa é inteligente, ele ignora a hora e salva apenas o dia correto (padrão ISO).
​P: A corretora coloca "BTC" junto com o número (ex: 0.005BTC). Tenho que apagar na mão?
R: Não! O programa tem uma função de limpeza que remove letras, cifrões (R$) e espaços automaticamente.
​P: E se eu importar o mesmo arquivo duas vezes sem querer?
R: O programa verifica se já existe uma compra com a mesma Data, Quantidade e Valor. Se existir, ele ignora e te avisa: "Duplicados (Ignorados): X".
​👨‍💻 Tecnologias Usadas
​Python 3: Linguagem base.
​Rich: Para a interface visual bonita (TUI).
​CSV & JSON: Manipulação nativa de dados.
​Feito para simplificar a gestão de Bitcoin. 🚀
