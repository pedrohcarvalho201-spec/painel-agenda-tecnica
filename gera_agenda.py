# -*- coding: utf-8 -*-
# Script: gera_agenda.py
# Propósito: Ler a agenda do arquivo .xlsx, processar os dados e gerar um arquivo HTML estático.

import pandas as pd
from jinja2 import Environment, FileSystemLoader

# --- Funções de Processamento de Dados ---

def ler_dados(caminho_planilha='agenda.xlsx'):
    """
    Lê o arquivo Excel da agenda, renomeia colunas e agrupa por técnico.
    """
    try:
        # Lendo o arquivo EXCEL (.xlsx)
        # O argumento 'encoding' foi removido, pois não é suportado por pd.read_excel()
        df = pd.read_excel(caminho_planilha, sheet_name=0) 
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_planilha}' não encontrado.")
        return None
    except Exception as e:
        print(f"ERRO ao ler a planilha Excel. Verifique se o 'openpyxl' está instalado. Detalhes: {e}")
        return None
    
    # 1. Ajuste: Renomear a coluna com acento ('Descrição') para um nome que o template entenda ('Descricao')
    if 'Descrição' in df.columns:
        df = df.rename(columns={'Descrição': 'Descricao'})
    
    # 2. Preenchimento de valores vazios com string vazia para evitar 'NaN' no HTML
    df = df.fillna('')

    # Prepara o dicionário de dados que será enviado ao HTML
    dados = {
        # Formata o horário atual para exibir no painel
        'data_atualizacao': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'),
        'tecnicos': {}
    }
    
    # Agrupa as linhas por Técnico
    for tecnico, grupo in df.groupby('Técnico'):
        # Garante que o nome do técnico não é vazio
        tecnico_str = str(tecnico).strip()
        if tecnico_str:
             # to_dict('records') transforma o grupo em uma lista de dicionários
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
    
    # 3. Salvamento do Arquivo HTML
    with open('agenda.html', 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print("---")
    print(f"✅ Sucesso! Arquivo agenda.html gerado às {dados_agenda['data_atualizacao']}")
    print("---")

if __name__ == "__main__":
    main()