# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import os

def consultar_diario():
    if not os.path.exists('historico_atendimentos.db'):
        print("❌ Histórico vazio ou inexistente.")
        return

    conn = sqlite3.connect('historico_atendimentos.db')
    
    # 1. Busca as datas disponíveis
    query_datas = "SELECT DISTINCT Data_Filtro FROM atendimentos_salvos ORDER BY Data_Hora_Registro DESC"
    try:
        datas_disponiveis = pd.read_sql_query(query_datas, conn)['Data_Filtro'].tolist()
    except:
        print("❌ Erro ao ler tabela. Certifique-se de que já salvou algum dia.")
        conn.close()
        return

    if not datas_disponiveis:
        print("Nenhum registro encontrado.")
        conn.close()
        return

    print("\n" + "="*40)
    print("📖 DIÁRIO DE ATENDIMENTOS (CONSULTA)")
    print("="*40)
    for i, data in enumerate(datas_disponiveis, 1):
        print(f"[{i}] - {data}")

    try:
        escolha = int(input("\nDigite o número da data desejada: "))
        data_selecionada = datas_disponiveis[escolha - 1]
        
        # 2. Busca os dados daquela data
        query_dados = f"SELECT * FROM atendimentos_salvos WHERE Data_Filtro = '{data_selecionada}'"
        df_dia = pd.read_sql_query(query_dados, conn)
        df_dia = df_dia.fillna('-') # Substitui vazios por traço

        print(f"\n" + "X"*60)
        print(f"📅 RELATÓRIO DETALHADO: {data_selecionada}")
        print("X"*60 + "\n")

        # 3. Impressão em formato de FICHA (Mais organizado para textos longos)
        for index, linha in df_dia.iterrows():
            # Só imprime se tiver cliente (ignora linhas apenas de kit se houver)
            if str(linha['Cliente']).strip() != '-':
                print(f"🔹 [{linha['Técnico']}] ID: {linha['ID']} | Cliente: {linha['Cliente']}")
                print(f"   Status: {linha['Status']}")
                
                if 'Cobranca' in linha and str(linha['Cobranca']).strip() != '-':
                    print(f"   Cobrança: {linha['Cobranca']}")
                
                if str(linha['Observação']).strip() != '-':
                    print(f"   📝 Obs: {linha['Observação']}")
                
                print("-" * 40) # Linha divisória entre atendimentos

        print(f"\n>>> Fim do relatório de {data_selecionada}. Total: {len(df_dia)} registros.")

    except (ValueError, IndexError):
        print("❌ Opção inválida.")
    
    conn.close()
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    consultar_diario()