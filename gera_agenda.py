# -*- coding: utf-8 -*-
# Script: gera_agenda.py - VERSAO FINAL E CORRIGIDA PARA NOVAS COLUNAS

import pandas as pd
from jinja2 import Environment, FileSystemLoader

# --- Funções de Processamento de Dados ---

def ler_dados(caminho_planilha='agenda.xlsx'):
    """
    Lê o arquivo Excel, forçando colunas críticas a serem lidas como texto (str).
    """
    try:
        # Colunas que DEVEM ser lidas como TEXTO (incluindo a nova 'Cobrança')
        dtype_config = {
            'ID': str, 'Técnico': str, 'Cliente': str, 
            'Descrição': str, 'Observação': str, 'Cobrança': str, 
            'Status': str
        }
        
        # Lendo o arquivo EXCEL (.xlsx)
        df = pd.read_excel(caminho_planilha, sheet_name=0, dtype=dtype_config) 
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_planilha}' não encontrado.")
        return None 
    except Exception as e:
        print(f"ERRO ao ler a planilha Excel. Detalhes: {e}")
        return None
    
    # --- Ajustes Pós-Leitura ---
    
    # Renomeia colunas com acento para o padrão do template (sem acento)
    if 'Descrição' in df.columns:
        df = df.rename(columns={'Descrição': 'Descricao'})
    if 'Observação' in df.columns:
        df = df.rename(columns={'Observação': 'Observacao'})
    if 'Cobrança' in df.columns: # <--- NOVO: RENOMEANDO COBRANÇA
        df = df.rename(columns={'Cobrança': 'Cobranca'})

    # Preenchimento de valores vazios com string vazia
    df = df.fillna('')
    
    # Prepara o dicionário de dados
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


# --- Funções de Geração de HTML (Sem alterações) ---

def gerar_html(dados):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    
    try:
        template = env.get_template('template_agenda.html')
    except Exception as e:
        print(f"ERRO: Não foi possível carregar o template_agenda.html. Detalhes: {e}")
        return None
    
    output = template.render(dados=dados)
    return output


def main():
    dados_agenda = ler_dados()
    if dados_agenda is None: return
        
    html_final = gerar_html(dados_agenda)
    if html_final is None: return
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print("---")
    print(f"✅ Sucesso! Arquivo index.html gerado às {dados_agenda['data_atualizacao']}")
    print("---")

if __name__ == "__main__":
    main()