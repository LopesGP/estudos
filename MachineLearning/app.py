import streamlit as st
import sqlite3
from detector_spam_regras import detectar_spam_por_regras

# Configurações da página
st.set_page_config(page_title="Detector de Spam por Regras", page_icon="📱")

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('spam_calls.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS numeros_spam (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL UNIQUE
)
''')
conn.commit()

# Título
st.title("📱 Detector de Spam por Regras")

# Função para verificar se um número é spam com base em regras adicionais
def verificar_regras_adicionais(numero):
    """Verifica se o número possui muitos dígitos repetidos ou é inválido."""
    numero_str = str(numero)
    
    # Verifica se o número possui muitos dígitos repetidos
    for digit in set(numero_str):
        if numero_str.count(digit) > 6:  # Ajuste o limite conforme necessário
            return 'Spam'
    
    # Verifica se o número tem um formato válido
    if len(numero_str) < 10 or len(numero_str) > 11:
        return 'Spam'
    
    return 'Não é Spam'

# Entrada do número de telefone
st.write("### Insira o número de telefone para verificar:")

# Criação de um campo de texto para entrada do número, apenas dígitos
numero_telefone = st.text_input("Número de Telefone", value="", max_chars=15)

# Filtrando a entrada para garantir que apenas números sejam aceitos
if not numero_telefone.isdigit() and numero_telefone != "":
    st.warning("Por favor, insira apenas números.")

# Botão para verificar
if st.button("Verificar"):
    if numero_telefone.isdigit() and len(numero_telefone) >= 10:  # Verifica se o número tem pelo menos 10 dígitos
        resultado_regras_adicionais = verificar_regras_adicionais(numero_telefone)
        resultado_detecção = detectar_spam_por_regras(int(numero_telefone))
        
        # Combina os resultados
        if resultado_regras_adicionais == 'Spam' or resultado_detecção == 'Spam':
            final_result = 'Spam'
            # Adiciona o número ao banco de dados
            try:
                cursor.execute("INSERT INTO numeros_spam (numero) VALUES (?)", (numero_telefone,))
                conn.commit()
            except sqlite3.IntegrityError:
                st.warning("Número já foi adicionado como spam.")
        else:
            final_result = 'Não é Spam'
        
        st.success(f"Resultado: **{final_result}**")
    else:
        st.error("Por favor, insira um número válido (pelo menos 10 dígitos).")

# Exibir a lista de números detectados como spam
st.write("### Números Recentemente Detectados como Spam:")
cursor.execute("SELECT numero FROM numeros_spam")
numeros_spam = cursor.fetchall()

if numeros_spam:
    for numero in numeros_spam:
        st.write(f"Número: {numero[0]}")
else:
    st.write("Nenhum número detectado como spam ainda.")

# Fechar a conexão ao banco de dados quando a aplicação for encerrada
conn.close()
