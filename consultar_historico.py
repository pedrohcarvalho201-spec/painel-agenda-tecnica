# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

def consultar():
    if not pd.io.common.file_exists('historico_atendimentos.db'):
        print("❌ Banco de dados ainda não existe. Salve o histórico primeiro!")
        return

    conn = sqlite3.connect('historico_atendimentos.db')
    
    # Query para ver o total de atendimentos por técnico e status ao longo do tempo
    query = """
    SELECT Data_Salvamento, Técnico, Status, COUNT(*) as Total
    FROM atendimentos_salvos
    GROUP BY Data_Salvamento, Técnico, Status
    ORDER BY Data_Salvamento DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    print("\n=== 📜 HISTÓRICO DE ATENDIMENTOS SALVOS ===")
    if df.empty:
        print("Nenhum dado encontrado.")
    else:
        # Mostra apenas os últimos 20 registros para não lotar a tela
        print(df.head(20).to_string(index=False))
        
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    consultar()