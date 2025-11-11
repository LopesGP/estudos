import pandas as pd

# Lista global para armazenar números detectados como spam
numeros_spam_recentes = []

# Lista de todos os prefixos válidos do Brasil
prefixos_validos_brasil = [
    '11', '12', '13', '14', '15', '16', '17', '18', '19',
    '21', '22', '24', '27', '28',
    '31', '32', '33', '34', '35', '37', '38',
    '41', '42', '43', '44', '45', '46',
    '51', '53', '54', '55',
    '61', '62', '63', '64',
    '65', '66', '67', '68', '69',
    '71', '73', '74', '75', '77',
    '81', '82', '83', '84', '85', '86', '87', '88',
    '91', '92', '93', '94', '95', '96', '97', '98', '99'
]

# Função para extrair prefixo e frequência do número
def extrair_dados(numero):
    """Extrai prefixo (código do estado) e frequência do número de telefone."""
    numero_str = str(numero)
    prefixo = numero_str[:2]  # Os dois primeiros dígitos após o código do país
    frequencia = len(numero_str)  # A frequência é o número de dígitos
    return frequencia, prefixo

# Função baseada em regras para detectar spam
def detectar_spam_por_regras(numero):
    """Avalia se um número é spam com base em regras definidas."""
    frequencia, prefixo = extrair_dados(numero)

    # Condições para determinar se é spam
    if prefixo not in prefixos_validos_brasil:
        resultado = 'Spam'  # Prefixo não reconhecido
    elif frequencia < 10 or frequencia > 15:  # Defina um intervalo válido de frequência
        resultado = 'Spam'  # Frequência inválida
    else:
        resultado = 'Não é Spam'

    # Se for spam, adiciona à lista de números detectados
    if resultado == 'Spam':
        numeros_spam_recentes.append(numero)

    return resultado

# Função para obter a lista de números detectados como spam
def obter_numeros_spam():
    """Retorna a lista de números recentemente detectados como spam."""
    return numeros_spam_recentes
