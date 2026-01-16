import sqlite3
from typing import List, Dict
import os

class LunaCache:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_recent_history(self, limit: int = 10) -> List[Dict[str, str]]:
        if not os.path.exists(self.db_path):
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Luna's cache structure as per ticket:
            # CREATE TABLE cache (srclang TEXT, tgtlang TEXT, source TEXT, trans TEXT);
            # We use rowid for ordering.
            cursor.execute(
                "SELECT source, trans FROM cache ORDER BY rowid DESC LIMIT ?", 
                (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            
            # Return in chronological order
            return [{"source": row[0], "trans": row[1]} for row in reversed(rows)]
        except Exception as e:
            print(f"Error reading Luna cache: {e}")
            return []

    def get_total_lines(self) -> int:
        if not os.path.exists(self.db_path):
            return 0
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cache")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0
