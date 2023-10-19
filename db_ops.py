import sqlite3


class Database:
    def __init__(self, db_name="flashcards.db"):
        self.db_name = db_name

    def insert_entry(self, table, **attributes): # working
        '''
        Create a new entry in the database.
        :param table: The name of the table in the database (e.g., 'decks' or 'cards').
        :param attributes: Dictionary of attribute names and their values for the new entry.
        '''
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Build the SQL query dynamically from the attributes
        columns = ', '.join(attributes.keys())
        placeholders = ', '.join(['?'] * len(attributes))
        insert_attributes = tuple(attributes.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, insert_attributes)

        conn.commit()
        conn.close()


    def update_entry(self, table, entry_id, **attributes): # working
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Build the SQL query dynamically from the provided attributes
            update_set = ', '.join([f"{key} = ?" for key in attributes.keys()])
            update_values = tuple(attributes.values())

            query = f"UPDATE {table} SET {update_set} WHERE id = ?"
            cursor.execute(query, (*update_values, entry_id))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")


    def delete_entry(self, table, entry_id): # working
        '''
        Delete an entry from the database based on its ID.
        :param table: The name of the table in the database (e.g., 'decks' or 'cards').
        :param entry_id: The ID of the entry to delete.
        '''
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Build the SQL query to delete the entry based on its ID
        query = f"DELETE FROM {table} WHERE id = ?"
        cursor.execute(query, (entry_id,))

        conn.commit()
        conn.close()

    def get_last_inserted_id(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        last_inserted_id = cursor.lastrowid

        conn.close()
        return last_inserted_id


# Not working properly
    def select_entries(self, table, conditions):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Construct the SQL query dynamically
        columns = ', '.join(conditions.keys())
        placeholders = ', '.join(['?'] * len(conditions))
        values = tuple(conditions.values())

        query = f"SELECT * FROM {table} WHERE {columns} = {placeholders}"
        cursor.execute(query, values)

        entries = cursor.fetchall()
        conn.close()

        # Transform the entries into dictionaries for easier access
        entries_dict = [dict(zip(conditions.keys(), entry)) for entry in entries]
        return entries_dict



conditions = {
    "deck_id": 31
}

# Create a Database instance (e.g., SQLiteDatabase)
db = Database()

# Call the select_entries method to retrieve the cards
selected_cards = db.select_entries("cards", conditions)

# Print the selected cards
for card in selected_cards:
    print(card)

