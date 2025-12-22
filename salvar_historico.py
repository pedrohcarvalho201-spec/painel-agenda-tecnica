# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
from datetime import datetime
import os

def realizar_backup_historico():
    caminho_planilha = 'agenda.xlsx'
    if not os.path.exists(caminho_planilha):
        print("❌ Erro: Planilha agenda.xlsx não encontrada!")
        return

    try:
        df = pd.read_excel(caminho_planilha, sheet_name=0)
        df = df.fillna('') 

        conn = sqlite3.connect('historico_atendimentos.db')
        
        # Criamos uma coluna de "Data_Filtro" apenas com o dia (para facilitar a busca)
        # E "Data_Hora_Registro" com o tempo exato do salvamento
        agora = datetime.now()
        df['Data_Filtro'] = agora.strftime('%d/%m/%Y')
        df['Data_Hora_Registro'] = agora.strftime('%d/%m/%Y %H:%M:%S')
        
        df.to_sql('atendimentos_salvos', conn, if_exists='append', index=False)
        conn.close()
        
        print(f"✅ FECHAMENTO CONCLUÍDO!")
        print(f"Dados salvos sob a data: {agora.strftime('%d/%m/%Y')}")
        input("\nPressione Enter para fechar...")

    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        input("Pressione Enter para fechar...")

if __name__ == "__main__":
    realizar_backup_historico()