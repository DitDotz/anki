import sqlite3


class Database:
    def __init__(self, db_name="flashcards.db"):
        self.db_name = db_name

    def insert_into_table(self, table, attributes):
        '''
        Insert a new entry in the database table.
        :param table: The name of the table in the database (e.g., 'decks' or 'cards').
        :param attributes: A dictionary of attribute names and their values for the new entry.
        
        Example usage
        insert_into_table('decks', {name:my_deck.name})
        '''
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        columns = ', '.join(attributes.keys())
        placeholders = ', '.join(['?'] * len(attributes))
        insert_values = tuple(attributes.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, insert_values)

        conn.commit()
        conn.close()
