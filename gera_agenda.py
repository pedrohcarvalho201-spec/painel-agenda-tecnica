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
            'Kit Faltando': str # <--- NOVA COLUNA NO EXCEL
        }
        df = pd.read_excel(caminho_planilha, sheet_name=0, dtype=dtype_config) 
    except Exception as e:
        print(f"ERRO ao ler planilha: {e}")
        return None
    
    # Padronização
    df = df.rename(columns={
        'Descrição': 'Descricao', 
        'Observação': 'Observacao', 
        'Cobrança': 'Cobranca', 
        'Ordens Abertas': 'OrdensAbertas',
        'Kit Faltando': 'KitFaltando'
    })
    df = df.fillna('')
    
    stats = {'total': 0, 'CONCLUIDO': 0, 'EM_ANDAMENTO': 0, 'PENDENTE': 0, 'FALHA': 0, 'por_tecnico': {}}
    kits_faltando = {} # Dicionário para armazenar kits por técnico

    df['Status_Clean'] = df['Status'].str.upper().str.replace(' ', '_')
    tecnicos_data = {}
    
    for tecnico, grupo in df.groupby('Técnico'):
        tecnico_str = str(tecnico).strip()
        if tecnico_str:
            # Pega o kit faltando do técnico (primeira linha encontrada dele)
            kit_info = grupo['KitFaltando'].replace('', pd.NA).dropna().iloc[0] if not grupo['KitFaltando'].replace('', pd.NA).dropna().empty else ""
            if kit_info:
                kits_faltando[tecnico_str] = kit_info

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

    ordens = df['OrdensAbertas'].iloc[0] if not df.empty and df['OrdensAbertas'].iloc[0] != "" else '0'
    
    return {
        'data_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'tecnicos': tecnicos_data,
        'stats': stats,
        'ordens_abertas_manual': ordens,
        'kits_faltando': kits_faltando # <--- ENVIANDO PARA O HTML
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
        print(f"🚀 Painel atualizado às {dados['data_atualizacao']}")

if __name__ == "__main__":
    main()