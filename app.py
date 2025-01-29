import os
import openai
import pdfplumber
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
openai.api_key = "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"

def process_email_with_gpt(email_text):
    prompt = f"""
    Você é um assistente especializado em classificar emails e sugerir respostas automáticas.

    **Critérios de Classificação**:
    1. **Produtivo**: Emails que requerem uma ação ou resposta específica.
        - Subcategorias:
            a. Suporte Técnico: Problemas técnicos ou dúvidas sobre o sistema.
            b. Atualização de Caso: Solicitações de atualização sobre casos, pedidos ou processos.
            c. Solicitação de Informação: Pedidos de informações sobre produtos, serviços ou documentos.
            d. Outro Produtivo: Outros emails que requerem ação.

    2. **Improdutivo**: Emails que não necessitam de ação.
        - Subcategorias:
            a. Agradecimento: Mensagens de agradecimento.
            b. Felicitação: Saudações ou mensagens de felicitação.
            c. Elogio: Feedback positivo ou elogios.
            d. Outro Improdutivo: Outros emails irrelevantes ou genéricos.

    **Instrução**:
    Classifique o seguinte email em uma das categorias e subcategorias acima, e sugira uma resposta, se aplicável.

    Email recebido:
    {email_text}

    Responda no seguinte formato:
    1. Categoria: Produtivo ou Improdutivo.
    2. Subcategoria: [Especifique a subcategoria].
    3. Resposta sugerida: [Forneça uma resposta ou diga "Sem resposta necessária" se for improdutivo].
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Ou gpt-4
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro ao processar o email: {str(e)}"

# Função para extrair texto de arquivos PDF e TXT
def extract_text_from_file(file):
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return ''.join([page.extract_text() for page in pdf.pages])
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_email():
    email_text = ''
    file = request.files.get('file')

    if file and file.filename:
        email_text = extract_text_from_file(file)
        if not email_text:
            return jsonify({'error': 'Arquivo inválido. Apenas arquivos .txt e .pdf são suportados.'}), 400
    elif 'email_text' in request.form and request.form['email_text'].strip():
        email_text = request.form['email_text']
    else:
        return jsonify({'error': 'Por favor, insira o texto do email ou envie um arquivo válido.'}), 400

    gpt_result = process_email_with_gpt(email_text)
    
    if "Erro ao processar" in gpt_result:
        return jsonify({'error': gpt_result}), 500

    return jsonify({'response': gpt_result})

if __name__ == '__main__':
    app.run(debug=True)
