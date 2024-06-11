# project-linkedin-bot
> Este projeto é um bot que responde automaticamente cada comentário das postagens das páginas de sua empresa que contenham uma determinada palavra-chave.

## 💻 Pré-requisitos
Antes de começar, tenha o navegador Google Chrome instalado.

## 🚀 Instalando o bot
### Para instalar a versão Python do bot
- Instale a versão 3.12 do Python. Instale [aqui](https://www.python.org/downloads/release/python-3124/).
- Clone o repositório em qualquer diretório do seu computador.
```
git clone https://github.com/danillo-de-paula-ss/project-linkedin-bot.git
```
- Dentro da pasta do repositório, abra um prompt e instale as dependências.
```
pip install -r requirements.txt
```
### Para instalar a versão Windows do bot
- Baixe a última versão do programa [aqui](https://github.com/danillo-de-paula-ss/project-linkedin-bot/releases).
- Descompacte o arquivo zip em qualquer diretório do seu computador.

## ☕ Usando o bot
Para usar o bot, execute o arquivo linkedin_bot.py (versão Python) ou linkedin_bot.exe (versão Windows).
Quando iniciar pela primeira vez, ele vai abrir uma janela perguntando se você deseja que o processo de login seja automático ou não. Imagem abaixo:

![image](https://github.com/danillo-de-paula-ss/project-linkedin-bot/blob/main/screenshots/initial_settings.png)

Se a escolha for automático, você deve inserir o usuário e a senha da conta do LinkedIn para que o bot possa fazer o login.
Uma vez feito o processo, o programa vai salvar as informações em um arquivo chamado "data.pkl", fechará a janela inicial e depois abrirá a janela principal para configuração do bot. E nas próximas vezes que for executar o programa, a janela para configurar o bot será a única a ser aberta. Imagem abaixo:

![image](https://github.com/danillo-de-paula-ss/project-linkedin-bot/blob/main/screenshots/main_program.png)
