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
        # 1. Lê os dados atuais da planilha
        df = pd.read_excel(caminho_planilha, sheet_name=0)
        df = df.fillna('') # Limpa campos vazios

        # 2. Conecta ao banco de dados (será criado se não existir)
        conn = sqlite3.connect('historico_atendimentos.db')
        
        # 3. Adiciona a data e hora do salvamento manual
        data_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['Data_Salvamento'] = data_registro
        
        # 4. Salva no banco de dados
        df.to_sql('atendimentos_salvos', conn, if_exists='append', index=False)
        conn.close()
        
        print(f"✅ SUCESSO! Dados de agora ({data_registro}) salvos no histórico.")
        input("Pressione Enter para fechar...") # Para você ver a mensagem de sucesso

    except Exception as e:
        print(f"❌ Ocorreu um erro ao salvar: {e}")
        input("Pressione Enter para fechar...")

if __name__ == "__main__":
    realizar_backup_historico()