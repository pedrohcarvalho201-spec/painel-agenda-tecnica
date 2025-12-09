# -*- coding: utf-8 -*-
# Script: gera_agenda.py
# Propósito: Ler a agenda do arquivo .xlsx, processar os dados e gerar um arquivo HTML estático (index.html).

import pandas as pd
from jinja2 import Environment, FileSystemLoader

# --- Funções de Processamento de Dados ---

def ler_dados(caminho_planilha='agenda.xlsx'):
    """
    Lê o arquivo Excel, forçando colunas críticas (ID, Descrição, Observação) 
    a serem lidas como texto (str) para preservar o formato e zeros.
    """
    try:
        # Colunas que DEVEM ser lidas como TEXTO (para preservar o zero e o formato)
        dtype_config = {
            'ID': str,
            'Técnico': str,
            'Cliente': str,
            # Leitura de 'Descrição' e 'Observação' como str para evitar problemas de tipo
            'Descrição': str,
            'Observação': str, 
            'Status': str
        }
        
        # Lendo o arquivo EXCEL (.xlsx) e aplicando a configuração de tipo
        df = pd.read_excel(caminho_planilha, sheet_name=0, dtype=dtype_config) 
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_planilha}' não encontrado.")
        return None 
    except Exception as e:
        print(f"ERRO ao ler a planilha Excel. Verifique se o 'openpyxl' está instalado. Detalhes: {e}")
        return None
    
    # --- Ajustes Pós-Leitura (Essenciais) ---
    
    # 1. Ajuste: Renomear colunas com acento para o padrão que o template entende (sem acento)
    if 'Descrição' in df.columns:
        df = df.rename(columns={'Descrição': 'Descricao'})
    
    if 'Observação' in df.columns:
        df = df.rename(columns={'Observação': 'Observacao'})

    # 2. Preenchimento de valores vazios com string vazia ('')
    # Isso é crucial para que o Jinja2 não falhe ou exiba 'NaN' no HTML.
    df = df.fillna('')
    
    # Prepara o dicionário de dados que será enviado ao HTML
    dados = {
        'data_atualizacao': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'),
        'tecnicos': {}
    }
    
    # Agrupa as linhas por Técnico
    for tecnico, grupo in df.groupby('Técnico'):
        tecnico_str = str(tecnico).strip()
        if tecnico_str:
             dados['tecnicos'][tecnico_str] = grupo.to_dict('records')
        
    return dados


# --- Funções de Geração de HTML ---

def gerar_html(dados):
    """
    Usa o Jinja2 para renderizar o template HTML com os dados fornecidos.
    """
    # O FileSystemLoader procura o arquivo 'template_agenda.html' no diretório atual
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    
    try:
        template = env.get_template('template_agenda.html')
    except Exception as e:
        print(f"ERRO: Não foi possível carregar o template_agenda.html. Verifique se ele está no mesmo diretório. Detalhes: {e}")
        return None
    
    # Renderiza o HTML final
    output = template.render(dados=dados)
    
    return output


# --- Função Principal ---

def main():
    """
    Função principal que orquestra a leitura e a geração do arquivo.
    """
    # 1. Leitura e Estruturação dos Dados
    dados_agenda = ler_dados()
    
    if dados_agenda is None:
        return # Interrompe se houver erro na leitura
        
    # 2. Geração do HTML
    html_final = gerar_html(dados_agenda)

    if html_final is None:
        return # Interrompe se houver erro na geração
    
    # 3. Salvamento do Arquivo HTML (Usando index.html para o GitHub Pages)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print("---")
    print(f"✅ Sucesso! Arquivo index.html gerado às {dados_agenda['data_atualizacao']}")
    print("---")

if __name__ == "__main__":
    main()