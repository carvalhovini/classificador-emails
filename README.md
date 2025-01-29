# Classificador de E-mails  

Este projeto é uma aplicação web que utiliza **Flask** e **OpenAI (GPT)** para classificar e-mails e sugerir respostas automáticas.  

## **Funcionalidades**  
- Classifica e-mails como **Produtivos** ou **Improdutivos**.  
- Sugere respostas automáticas para e-mails produtivos.  
- Permite inserção manual de texto ou upload de arquivos **.txt** e **.pdf**.  

## **Instalação e Execução**  

1. **Clonar o repositório:**  
   ```bash
   git clone https://github.com/carvalhovini/classificador-emails.git
   cd classificador-emails

Criar um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

Instalar as dependências:
pip install -r requirements.txt

Executar o servidor:
python app.py
Acesse no navegador: http://127.0.0.1:5000/

Como Usar

Insira o texto do e-mail ou faça upload de um arquivo .txt ou .pdf.
Clique em "Classificar Email".
O sistema exibirá a categoria e a resposta sugerida.
