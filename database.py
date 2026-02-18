import sqlite3
from typing import List, Optional
from datetime import datetime
from models import Campaign


class Database:
    def __init__(self, db_path: str = "launch_kit.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                channel TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT,
                posted_at TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()
    
    def save_campaign(self, campaign: Campaign) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO campaigns (product_name, channel, title, url, posted_at, clicks, conversions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            campaign.product_name,
            campaign.channel,
            campaign.title,
            campaign.url,
            campaign.posted_at.isoformat(),
            campaign.clicks or 0,
            campaign.conversions or 0
        ))
        conn.commit()
        campaign_id = cursor.lastrowid
        conn.close()
        return campaign_id
    
    def update_campaign_metrics(self, campaign_id: int, clicks: Optional[int], conversions: Optional[int]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if clicks is not None:
            cursor.execute("UPDATE campaigns SET clicks = ? WHERE id = ?", (clicks, campaign_id))
        if conversions is not None:
            cursor.execute("UPDATE campaigns SET conversions = ? WHERE id = ?", (conversions, campaign_id))
        
        conn.commit()
        conn.close()
    
    def get_campaigns(self, product_name: Optional[str] = None) -> List[Campaign]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if product_name:
            cursor.execute("SELECT * FROM campaigns WHERE product_name = ? ORDER BY posted_at DESC", (product_name,))
        else:
            cursor.execute("SELECT * FROM campaigns ORDER BY posted_at DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        campaigns = []
        for row in rows:
            campaigns.append(Campaign(
                id=row[0],
                product_name=row[1],
                channel=row[2],
                title=row[3],
                url=row[4],
                posted_at=datetime.fromisoformat(row[5]),
                clicks=row[6],
                conversions=row[7]
            ))
        
        return campaigns
