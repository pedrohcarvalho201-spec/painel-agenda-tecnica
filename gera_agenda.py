# -*- coding: utf-8 -*-
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def ler_dados(caminho_planilha='agenda.xlsx'):
    try:
        dtype_config = {
            'ID': str, 'Técnico': str, 'Cliente': str, 
            'Descrição': str, 'Observação': str, 'Cobrança': str, 
            'Status': str, 'Ordens Abertas': str,
            'Kit Faltando': str
        }
        df = pd.read_excel(caminho_planilha, sheet_name=0, dtype=dtype_config) 
    except Exception as e:
        print(f"ERRO ao ler planilha: {e}")
        return None
    
    # Padronização de nomes de colunas
    df = df.rename(columns={
        'Descrição': 'Descricao', 
        'Observação': 'Observacao', 
        'Cobrança': 'Cobranca', 
        'Ordens Abertas': 'OrdensAbertas',
        'Kit Faltando': 'KitFaltando'
    })
    df = df.fillna('')
    
    stats = {'total': 0, 'CONCLUIDO': 0, 'EM_ANDAMENTO': 0, 'PENDENTE': 0, 'FALHA': 0, 'por_tecnico': {}}
    kits_faltando = {} 

    # 1. Coletar informações de Kits de TODOS os técnicos antes de filtrar tarefas
    for tecnico, grupo in df.groupby('Técnico'):
        tecnico_str = str(tecnico).strip()
        if tecnico_str and tecnico_str.lower() != 'nan':
            # Procura qualquer menção de kit para este técnico na planilha toda
            kit_info = grupo['KitFaltando'].replace('', pd.NA).dropna().iloc[0] if not grupo['KitFaltando'].replace('', pd.NA).dropna().empty else ""
            if kit_info:
                kits_faltando[tecnico_str] = kit_info

    # 2. Filtrar o DataFrame: Manter apenas linhas que possuam Cliente ou ID (tarefas REAIS)
    # Isso remove os técnicos que só estão na planilha para acusar o kit
    df_tarefas = df[df['Cliente'].str.strip() != ''].copy()

    df_tarefas['Status_Clean'] = df_tarefas['Status'].str.upper().str.replace(' ', '_')
    tecnicos_data = {}
    
    # 3. Processar apenas os técnicos que possuem tarefas reais para as colunas e estatísticas
    for tecnico, grupo in df_tarefas.groupby('Técnico'):
        tecnico_str = str(tecnico).strip()
        if tecnico_str:
            g_stats = grupo['Status_Clean'].value_counts().to_dict()
            t_stats = {
                'total': len(grupo),
                'CONCLUIDO': g_stats.get('CONCLUIDO', 0),
                'EM_ANDAMENTO': g_stats.get('EM_ANDAMENTO', 0),
                'PENDENTE': g_stats.get('PENDENTE', 0),
                'FALHA': g_stats.get('FALHA', 0)
            }
            stats['por_tecnico'][tecnico_str] = t_stats
            stats['total'] += t_stats['total']
            stats['CONCLUIDO'] += t_stats['CONCLUIDO']
            stats['EM_ANDAMENTO'] += t_stats['EM_ANDAMENTO']
            stats['PENDENTE'] += t_stats['PENDENTE']
            stats['FALHA'] += t_stats['FALHA']
            
            tecnicos_data[tecnico_str] = grupo.to_dict('records')

    # Pega o valor das Ordens Abertas (da planilha original, caso esteja em uma linha sem tarefa)
    ordens = df['OrdensAbertas'].replace('', pd.NA).dropna().iloc[0] if not df['OrdensAbertas'].replace('', pd.NA).dropna().empty else '0'
    
    return {
        'data_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'tecnicos': tecnicos_data,
        'stats': stats,
        'ordens_abertas_manual': ordens,
        'kits_faltando': kits_faltando
    }

def gerar_html(dados):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('template_agenda.html')
    return template.render(dados=dados)

def main():
    dados = ler_dados()
    if dados:
        html = gerar_html(dados)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"🚀 Painel atualizado com filtro de tarefas ativado às {dados['data_atualizacao']}")

if __name__ == "__main__":
    main()