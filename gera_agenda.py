# -*- coding: utf-8 -*-
# Script: gera_agenda.py - VERSAO FINAL E CORRIGIDA PARA NOVAS COLUNAS E ESTATÍSTICAS

import pandas as pd
from jinja2 import Environment, FileSystemLoader

# --- Funções de Processamento de Dados ---

def ler_dados(caminho_planilha='agenda.xlsx'):
    """
    Lê o arquivo Excel, processa dados, calcula estatísticas e agrupa por técnico.
    """
    try:
        # Colunas que DEVEM ser lidas como TEXTO (incluindo as novas)
        dtype_config = {
            'ID': str, 'Técnico': str, 'Cliente': str, 
            'Descrição': str, 'Observação': str, 'Cobrança': str, 
            'Status': str, 'Ordens Abertas': str # <--- NOVO: Leitura da Coluna Ordens Abertas
        }
        
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
    if 'Cobrança' in df.columns:
        df = df.rename(columns={'Cobrança': 'Cobranca'})
    
    # Renomeia a coluna que você adicionará
    if 'Ordens Abertas' in df.columns:
        df = df.rename(columns={'Ordens Abertas': 'OrdensAbertas'})

    # Preenchimento de valores vazios com string vazia
    df = df.fillna('')
    
    # --- Cálculo de Estatísticas ---
    
    stats = {
        'total': 0,
        'CONCLUIDO': 0,
        'EM_ANDAMENTO': 0,
        'PENDENTE': 0,
        'por_tecnico': {}
    }
    
    # Converte a coluna Status para maiúsculas e substitui espaços
    df['Status_Clean'] = df['Status'].str.upper().str.replace(' ', '_')
    
    tecnicos_data = {}
    
    for tecnico, grupo in df.groupby('Técnico'):
        tecnico_str = str(tecnico).strip()
        if tecnico_str:
            grupo_stats = grupo['Status_Clean'].value_counts().to_dict()
            
            # Garante que todas as chaves de status existem
            tecnico_stats = {
                'total': len(grupo),
                'CONCLUIDO': grupo_stats.get('CONCLUIDO', 0),
                'EM_ANDAMENTO': grupo_stats.get('EM_ANDAMENTO', 0),
                'PENDENTE': grupo_stats.get('PENDENTE', 0),
                'BLOQUEADO': grupo_stats.get('BLOQUEADO', 0) # Mantendo bloqueado para cálculo, mesmo sem legenda
            }
            
            stats['por_tecnico'][tecnico_str] = tecnico_stats
            
            # Acumula total geral
            stats['total'] += tecnico_stats['total']
            stats['CONCLUIDO'] += tecnico_stats['CONCLUIDO']
            stats['EM_ANDAMENTO'] += tecnico_stats['EM_ANDAMENTO']
            stats['PENDENTE'] += tecnico_stats['PENDENTE']
            
            tecnicos_data[tecnico_str] = grupo.to_dict('records')

    # Pega o valor da coluna 'Ordens Abertas' (assumindo que o valor é o mesmo em todas as linhas, pegamos o primeiro não vazio)
    ordens_abertas_manual = df['OrdensAbertas'].replace('', pd.NA).dropna().iloc[0] if not df['OrdensAbertas'].empty and not df['OrdensAbertas'].replace('', pd.NA).dropna().empty else 'N/A'
    
    # Prepara o dicionário de dados final
    dados = {
        'data_atualizacao': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'),
        'tecnicos': tecnicos_data,
        'stats': stats,
        'ordens_abertas_manual': ordens_abertas_manual
    }
    
    return dados


# --- Funções de Geração de HTML (As mesmas) ---

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