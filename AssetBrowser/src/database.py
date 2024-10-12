import sqlite3

class AssetDatabase:
    def __init__(self, db_path='assets.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT,
                thumbnail_path TEXT,
                metadata TEXT
            )""")
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT
            )""")
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS asset_tags (
                asset_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (asset_id) REFERENCES assets (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )""")

    def add_asset(self, name, path, thumbnail_path, metadata):
        with self.conn:
            self.conn.execute("INSERT INTO assets (name, path, thumbnail_path, metadata) VALUES (?, ?, ?, ?)", (name, path, thumbnail_path, metadata))

    def search_assets(self, keyword):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM assets WHERE name LIKE ?", (f'%{keyword}%',))
        return cur.fetchall()

    def close(self):
        self.conn.close()
