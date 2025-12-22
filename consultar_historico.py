# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

def consultar_diario():
    if not pd.io.common.file_exists('historico_atendimentos.db'):
        print("❌ Histórico vazio ou inexistente.")
        return

    conn = sqlite3.connect('historico_atendimentos.db')
    
    # 1. Busca todas as datas únicas que existem no banco
    query_datas = "SELECT DISTINCT Data_Filtro FROM atendimentos_salvos ORDER BY Data_Hora_Registro DESC"
    datas_disponiveis = pd.read_sql_query(query_datas, conn)['Data_Filtro'].tolist()

    if not datas_disponiveis:
        print("Nenhum registro encontrado.")
        conn.close()
        return

    print("\n--- 📖 DIÁRIO DE ATENDIMENTOS ---")
    print("Datas disponíveis no histórico:")
    for i, data in enumerate(datas_disponiveis, 1):
        print(f"[{i}] - {data}")

    try:
        escolha = int(input("\nDigite o número da data que deseja consultar: "))
        data_selecionada = datas_disponiveis[escolha - 1]
        
        # 2. Busca os dados daquela data específica
        query_dados = f"SELECT * FROM atendimentos_salvos WHERE Data_Filtro = '{data_selecionada}'"
        df_dia = pd.read_sql_query(query_dados, conn)
        
        # 3. Exibe o "Relatório do Dia"
        print(f"\n==========================================")
        print(f"📅 RELATÓRIO DO DIA: {data_selecionada}")
        print(f"==========================================\n")
        
        # Organiza a exibição (pode ajustar as colunas que quer ver aqui)
        colunas_exibir = ['Técnico', 'ID', 'Cliente', 'Status', 'Cobrança', 'Observação']
        # Filtramos apenas as colunas que existem no DF para evitar erros
        colunas_existentes = [c for c in colunas_exibir if c in df_dia.columns]
        
        print(df_dia[colunas_existentes].to_string(index=False))
        
        print(f"\nTotal de registros salvos neste dia: {len(df_dia)}")

    except (ValueError, IndexError):
        print("❌ Opção inválida.")
    
    conn.close()
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    consultar_diario()