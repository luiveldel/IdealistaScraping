import sqlite3
import os

class ApiDatabase:
    
    api_key: str
    db_path: str
    
    def __init__(self, api_key, db_path):
        self.api_key = api_key
        if db_path is None:
            # If no path is specified, use the current working directory
            db_path = os.path.join(os.getcwd(), 'api_data.db')
        self.db_file = db_path
        self.conn = None

    def connect(self):
        # Connect to the database and create a table if it doesn't already exist
        # conn = sqlite3.connect('api_data.db')
        self.conn = sqlite3.connect(self.db_file)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS api_data
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      url TEXT,
                      response TEXT)''')
        self.conn.commit()

    def make_request(self, url, response):
        c = self.conn.cursor()
        c.execute("SELECT * FROM api_data WHERE url = ? AND response = ?", (url, response.text))
        result = c.fetchone()
        if result is None:
            c.execute("INSERT INTO api_data (url, response) VALUES (?, ?)", (url, response.text))
            self.conn.commit()
  

    def close(self):
        # Close the database connection
        if self.conn is not None:
            self.conn.close()
