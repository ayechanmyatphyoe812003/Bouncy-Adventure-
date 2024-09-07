# database.py

import sqlite3

def connect_db():
    return sqlite3.connect('user_data.db')

def add_current_level_column():
    conn = connect_db()
    cursor = conn.cursor()

    # Add a new column to the users table
    cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS current_level INTEGER DEFAULT 0")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def save_player_progress(player_id, current_level):
    conn = connect_db()
    cursor = conn.cursor()

    # Update the player's current level
    cursor.execute("UPDATE users SET current_level = ? WHERE id = ?", (current_level, player_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def load_player_progress(player_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Retrieve the player's current level
    cursor.execute("SELECT current_level FROM users WHERE id = ?", (player_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the current level
    else:
        return 0  # Default to level 0 if player data not found
