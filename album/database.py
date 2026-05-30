import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'album.db')
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

def criar_tabela():
    """Cria o banco de dados na primeira execução"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unlocked_cards (
            player_name TEXT,
            card_id     TEXT,
            PRIMARY KEY (player_name, card_id)
            )
        ''')
    
def unlock_card(player_name, card_id):
    """Setar na tabela do DB a carta desbloqueada e o player que desbloqueou"""
    cursor.execute('INSERT OR IGNORE INTO unlocked_cards VALUES (?, ?)', (player_name, card_id))
    connection.commit()


def get_unlocked_cards(player_name):
    rows = cursor.execute('SELECT card_id FROM unlocked_cards WHERE player_name = ?', (player_name, ))
    cartas = set()
    for row in rows:
        cartas.add(row[0])
    return cartas


