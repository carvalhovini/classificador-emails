import os
import pdfplumber
from openai import OpenAI
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Obtendo a chave da OpenAI da variável de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Erro: OPENAI_API_KEY não foi encontrada. Configure no Render.")

# Criando um cliente OpenAI corretamente
client = OpenAI(api_key=openai_api_key)

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
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao processar o email: {str(e)}"

# Função para extrair texto de arquivos PDF e TXT
def extract_text_from_file(file):
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            text = '\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])
            return text.strip() if text else None
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
    # Tornando o servidor compatível com plataformas de hospedagem
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
