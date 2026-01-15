import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from config import Config

class DBConnector:
    def __init__(self):
        self.config = Config()
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(
            host=self.config.DB_HOST,
            port=self.config.DB_PORT,
            database=self.config.DB_NAME,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
    
    def execute_query(self, query, params=None):
        """Execute SQL query and return results as list of dicts"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                results = cursor.fetchall()
            return results
        finally:
            conn.close()
    
    def get_dataframe(self, query, params=None):
        """Execute query and return pandas DataFrame"""
        conn = self.get_connection()
        try:
            return pd.read_sql_query(query, conn, params=params)
        finally:
            conn.close()
    
    # Specific queries for your Django database
    
    def get_all_tracks(self):
        """Get all music tracks with genres"""
        query = """
        SELECT 
            mt.id, mt.title, mt.artist, mt.duration, mt.bpm,
            g.name as genre, mt.duration
        FROM repertoire_musictrack mt
        LEFT JOIN repertoire_genre g ON mt.genre_id = g.id
        ORDER BY mt.title
        """
        return self.execute_query(query)
    
    def get_repertoire_schedule(self):
        """Get repertoire schedule with details"""
        query = """
        SELECT 
            r.id, r.start_time, r.end_time, r.date,
            mt.title as track_title, mt.artist, mt.duration, mt.bpm,
            g.name as genre,
            h.name as hall_name, h.capacity,
            w.name as weekday,
            ho.name as host_name, ho.experience
        FROM repertoire_repertoire r
        JOIN repertoire_musictrack mt ON r.music_track_id = mt.id
        LEFT JOIN repertoire_genre g ON mt.genre_id = g.id
        JOIN repertoire_hall h ON r.hall_id = h.id
        JOIN repertoire_weekday w ON r.day_id = w.id
        JOIN repertoire_host ho ON r.host_id = ho.id
        ORDER BY r.date, r.start_time
        """
        return self.execute_query(query)
    
    def get_statistics(self):
        """Get various statistics"""
        stats = {}
        
        # Total tracks by genre
        query = """
        SELECT g.name as genre, COUNT(*) as count
        FROM repertoire_musictrack mt
        JOIN repertoire_genre g ON mt.genre_id = g.id
        GROUP BY g.name
        ORDER BY count DESC
        """
        stats['tracks_by_genre'] = self.execute_query(query)
        
        # Busiest weekdays
        query = """
        SELECT w.name as weekday, COUNT(*) as sessions
        FROM repertoire_repertoire r
        JOIN repertoire_weekday w ON r.day_id = w.id
        GROUP BY w.id, w.name
        ORDER BY w.id
        """
        stats['sessions_by_weekday'] = self.execute_query(query)
        
        # Host performance
        query = """
        SELECT 
            ho.name as host_name,
            ho.experience,
            COUNT(DISTINCT r.id) as sessions_hosted,
            COUNT(DISTINCT r.music_track_id) as unique_tracks,
            AVG(mt.bpm) as avg_bpm
        FROM repertoire_repertoire r
        JOIN repertoire_host ho ON r.host_id = ho.id
        JOIN repertoire_musictrack mt ON r.music_track_id = mt.id
        GROUP BY ho.id, ho.name, ho.experience
        ORDER BY sessions_hosted DESC
        """
        stats['host_performance'] = self.execute_query(query)
        
        # Hall utilization
        query = """
        SELECT 
            h.name as hall, h.capacity,
            COUNT(DISTINCT r.id) as total_sessions,
            COUNT(DISTINCT r.day_id) as days_used
        FROM repertoire_repertoire r
        JOIN repertoire_hall h ON r.hall_id = h.id
        GROUP BY h.id, h.name, h.capacity
        ORDER BY total_sessions DESC
        """
        stats['hall_utilization'] = self.execute_query(query)
        
        # Artists statistics
        query = """
        SELECT 
            mt.artist,
            COUNT(*) as track_count,
            AVG(mt.bpm) as avg_bpm,
            SUM(EXTRACT(EPOCH FROM mt.duration)) / 60 as total_minutes
        FROM repertoire_musictrack mt
        GROUP BY mt.artist
        ORDER BY track_count DESC
        LIMIT 10
        """
        stats['top_artists'] = self.execute_query(query)
        
        return stats
    
    def get_daily_analysis(self):
        """Analyze tracks throughout the day"""
        query = """
        SELECT 
            EXTRACT(HOUR FROM r.start_time) as hour,
            COUNT(*) as tracks_count,
            AVG(mt.bpm) as avg_bpm
        FROM repertoire_repertoire r
        JOIN repertoire_musictrack mt ON r.music_track_id = mt.id
        GROUP BY EXTRACT(HOUR FROM r.start_time)
        ORDER BY hour
        """
        return self.execute_query(query)
    
    def search_tracks(self, search_term):
        """Search tracks by title, artist or genre"""
        query = """
        SELECT 
            mt.id, mt.title, mt.artist, mt.duration, mt.bpm,
            g.name as genre,
            COUNT(r.id) as play_count
        FROM repertoire_musictrack mt
        LEFT JOIN repertoire_genre g ON mt.genre_id = g.id
        LEFT JOIN repertoire_repertoire r ON mt.id = r.music_track_id
        WHERE mt.title ILIKE %s OR mt.artist ILIKE %s OR g.name ILIKE %s
        GROUP BY mt.id, g.name
        ORDER BY mt.title
        """
        search_pattern = f'%{search_term}%'
        return self.execute_query(query, (search_pattern, search_pattern, search_pattern))
    
    def get_upcoming_schedule(self, days=7):
        """Get upcoming schedule for next N days"""
        query = """
        SELECT 
            r.date, r.start_time, r.end_time,
            mt.title, mt.artist,
            h.name as hall,
            w.name as weekday,
            ho.name as host
        FROM repertoire_repertoire r
        JOIN repertoire_musictrack mt ON r.music_track_id = mt.id
        JOIN repertoire_hall h ON r.hall_id = h.id
        JOIN repertoire_weekday w ON r.day_id = w.id
        JOIN repertoire_host ho ON r.host_id = ho.id
        WHERE r.date >= CURRENT_DATE 
        AND r.date <= CURRENT_DATE + INTERVAL '%s days'
        ORDER BY r.date, r.start_time
        """
        return self.execute_query(query, (days,))
