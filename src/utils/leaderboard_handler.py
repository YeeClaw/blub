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
import logging

logger = logging.getLogger(__name__)

class LeaderboardHandler:
    def __init__(self):
        self.host = os.environ.get("DB_HOST")
        self.database = os.environ.get("DB_NAME")
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PASS")

        self._conn = None
        self._cursor = None

    def manage_connection(self):
        if not self._conn or self._conn.closed:
            self._conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self._cursor = self._conn.cursor()
            logger.info("Postgres connection established.")
        else:
            self._conn.close()
            self._cursor.close()
            logger.info("Postgres connection closed.")

    def get_highscore(self, user_id: int, activity_id: int):
        self._cursor.execute(
            f"""
            SELECT score 
            FROM blub.highscore 
            WHERE user_id = {user_id} AND 
                activity_id = {activity_id}
            ORDER BY score DESC
            """
        )
        logger.info(f"Highscore for user {user_id} and activity {activity_id} fetched.")
        return self._cursor.fetchone()

    def update_highscore(self, user_id: int, activity_id: int, new_score: int) -> bool:
        recieved_best = self.get_highscore(user_id, activity_id)
        if recieved_best:
            current_best = recieved_best[0]
        else:
            current_best = -1

        if new_score < current_best or current_best == -1:
            self._cursor.execute(
                f"""
                INSERT INTO blub.highscore (user_id, activity_id, score)
                VALUES ({user_id}, {activity_id}, {new_score})
                """
            )
            self._conn.commit()
            logger.info(f"Highscore for user {user_id} and activity {activity_id} updated.")
            return True
        logger.info(f"Highscore for user {user_id} and activity {activity_id} not updated.")
        return False

    def generate_leaderboard(self, activity_id: int, limit: int):
        self._cursor.execute(
            f"""
            SELECT user_id, score
            FROM blub.highscore
            WHERE activity_id = {activity_id}
            ORDER BY score
            LIMIT {limit}
            """
        )
        leaders = self._cursor.fetchall()
        logger.info(f"Leaderboard for activity {activity_id} generated.")
        return leaders

    def __del__(self):
        if self._conn:
            self._conn.close()
            self._cursor.close()
            logger.info("Postgres connection closed.")
