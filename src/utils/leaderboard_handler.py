"""
What do I do?
-------------
1. Collect highscore results
2. Compare highscore results
3. Update highscore results
4. Generate leaderboard content

A db.highscore record contains the following:
-------------------------------------------------------
|highscore_id | member_id | score | activity_id | date|
-------------------------------------------------------
"""

import os
import psycopg2

class LeaderboardHandler:
    def __init__(self):
        self.host = os.environ.get("DB_HOST")
        self.database = os.environ.get("DB_NAME")
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PASS")

    def get_highscore(self):
        pass

    def compare_scores(self):
        pass

    def update_highscore(self):
        pass

    def generate_leaderboard(self):
        pass
