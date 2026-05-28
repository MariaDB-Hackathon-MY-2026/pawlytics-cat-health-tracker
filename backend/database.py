"""
Database Module
Handles all MariaDB interactions with connection pooling and error handling
"""

import mysql.connector
from mysql.connector import Error, pooling
from typing import Optional, Dict, List, Any, Tuple
import logging
from datetime import datetime, date
from .config import Config

# Setup logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class Database:
    """Database connection and query management"""
    
    _connection_pool: Optional[pooling.MySQLConnectionPool] = None
    
    def __init__(self):
        """Initialize database connection pool"""
        if Database._connection_pool is None:
            self._create_connection_pool()
    
    def _create_connection_pool(self):
        """Create MySQL connection pool for better performance"""
        try:
            Database._connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="pawlytics_pool",
                pool_size=Config.DB_POOL_SIZE,
                pool_reset_session=True,
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                autocommit=False
            )
            logger.info("✅ Database connection pool created successfully")
        except Error as e:
            logger.error(f"❌ Failed to create connection pool: {e}")
            raise
    
    def get_connection(self):
        """
        Get connection from pool
        Returns: MySQL connection object or None
        """
        try:
            if Database._connection_pool:
                conn = Database._connection_pool.get_connection()
                return conn
            else:
                logger.error("Connection pool not initialized")
                return None
        except Error as e:
            logger.error(f"❌ Error getting connection: {e}")
            return None
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Tuple] = None, 
        fetch_one: bool = False
    ) -> Optional[Any]:
        """
        Execute SELECT query with automatic connection management
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            fetch_one: If True, return single row; else return all rows
        
        Returns:
            Query results as list of dictionaries or single dictionary
        """
        conn = None
        cursor = None
        
        try:
            conn = self.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            
            return result
            
        except Error as e:
            logger.error(f"❌ Query execution error: {e}")
            logger.error(f"Query: {query}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def execute_update(
        self, 
        query: str, 
        params: Optional[Tuple] = None
    ) -> Optional[int]:
        """
        Execute INSERT/UPDATE/DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
        
        Returns:
            Last inserted ID for INSERT, affected rows for UPDATE/DELETE
        """
        conn = None
        cursor = None
        
        try:
            conn = self.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            
            # Return last insert ID or affected rows
            if query.strip().upper().startswith('INSERT'):
                result = cursor.lastrowid
            else:
                result = cursor.rowcount
            
            logger.info(f"✅ Update successful: {result} rows affected")
            return result
            
        except Error as e:
            logger.error(f"❌ Update execution error: {e}")
            logger.error(f"Query: {query}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    # ==========================================
    # KIBBLE OPERATIONS
    # ==========================================
    
    def insert_kibble(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Insert or update kibble data
        
        Args:
            data: Dictionary with keys: brand_name, protein_pct, fat_pct, 
                  fiber_pct, moisture_pct, price_per_kg, rating
        
        Returns:
            Kibble ID or None on failure
        """
        query = """
            INSERT INTO kibbles 
            (brand_name, product_line, protein_pct, fat_pct, fiber_pct, 
             moisture_pct, ash_pct, price_per_kg, rating, 
             ingredients_list, has_grain, aafco_approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                protein_pct = VALUES(protein_pct),
                fat_pct = VALUES(fat_pct),
                fiber_pct = VALUES(fiber_pct),
                moisture_pct = VALUES(moisture_pct),
                ash_pct = VALUES(ash_pct),
                price_per_kg = VALUES(price_per_kg),
                rating = VALUES(rating),
                ingredients_list = VALUES(ingredients_list),
                updated_at = CURRENT_TIMESTAMP
        """
        
        params = (
            data.get('brand_name'),
            data.get('product_line', 'General'),
            data.get('protein_pct'),
            data.get('fat_pct'),
            data.get('fiber_pct'),
            data.get('moisture_pct'),
            data.get('ash_pct', 0.0),
            data.get('price_per_kg', 0.0),
            data.get('rating'),
            data.get('ingredients_list', ''),
            data.get('has_grain', False),
            data.get('aafco_approved', False)
        )
        
        return self.execute_update(query, params)
    
    def get_kibble_by_id(self, kibble_id: int) -> Optional[Dict]:
        """Fetch single kibble by ID"""
        query = "SELECT * FROM kibbles WHERE id = %s"
        return self.execute_query(query, (kibble_id,), fetch_one=True)
    
    def get_all_kibbles(self) -> List[Dict]:
        """Fetch all kibbles"""
        query = "SELECT * FROM kibbles ORDER BY rating ASC, protein_pct DESC"
        return self.execute_query(query) or []
    
    def search_kibbles(self, search_term: str) -> List[Dict]:
        """Search kibbles by brand name"""
        query = """
            SELECT * FROM kibbles 
            WHERE brand_name LIKE %s OR product_line LIKE %s
            ORDER BY rating ASC
        """
        pattern = f"%{search_term}%"
        return self.execute_query(query, (pattern, pattern)) or []
    
    # ==========================================
    # CAT OPERATIONS
    # ==========================================
    
    def insert_cat(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Insert cat profile
        
        Args:
            data: Dictionary with cat details
        
        Returns:
            Cat ID or None on failure
        """
        query = """
            INSERT INTO cats 
            (name, age_months, weight_kg, gender, neutered, 
             condition_score, bcs_numeric, activity_level, 
             health_conditions, owner_name, contact_email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data.get('name'),
            data.get('age_months'),
            data.get('weight_kg'),
            data.get('gender', 'Unknown'),
            data.get('neutered', False),
            data.get('condition_score', 'Ideal'),
            data.get('bcs_numeric', 5),
            data.get('activity_level', 'Moderate'),
            data.get('health_conditions', ''),
            data.get('owner_name', ''),
            data.get('contact_email', '')
        )
        
        return self.execute_update(query, params)
    
    def get_cat_by_id(self, cat_id: int) -> Optional[Dict]:
        """Fetch single cat profile"""
        query = "SELECT * FROM cats WHERE id = %s"
        return self.execute_query(query, (cat_id,), fetch_one=True)
    
    def get_all_cats(self) -> List[Dict]:
        """Fetch all cat profiles"""
        query = "SELECT * FROM cats ORDER BY created_at DESC"
        return self.execute_query(query) or []
    
    def update_cat_weight(self, cat_id: int, new_weight: float) -> bool:
        """Update cat's weight"""
        query = "UPDATE cats SET weight_kg = %s WHERE id = %s"
        result = self.execute_update(query, (new_weight, cat_id))
        return result is not None
    
    # ==========================================
    # FEEDING LOG OPERATIONS
    # ==========================================
    
    def insert_feeding_log(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Log a feeding event
        
        Args:
            data: Dictionary with feeding details
        
        Returns:
            Log ID or None on failure
        """
        query = """
            INSERT INTO feeding_logs 
            (cat_id, kibble_id, date_recorded, meal_time, amount_grams, appetite, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data.get('cat_id'),
            data.get('kibble_id'),
            data.get('date_recorded', date.today()),
            data.get('meal_time', 'Dinner'),
            data.get('amount_grams', 0),
            data.get('appetite', 'Normal'),
            data.get('notes', '')
        )
        
        return self.execute_update(query, params)
    
    def get_feeding_logs_by_cat(
        self, 
        cat_id: int, 
        limit: int = 30
    ) -> List[Dict]:
        """Get recent feeding logs for a specific cat"""
        query = """
            SELECT fl.*, k.brand_name, k.protein_pct
            FROM feeding_logs fl
            JOIN kibbles k ON fl.kibble_id = k.id
            WHERE fl.cat_id = %s
            ORDER BY fl.date_recorded DESC
            LIMIT %s
        """
        return self.execute_query(query, (cat_id, limit)) or []
    
    # ==========================================
    # ANALYTICS
    # ==========================================
    
    def get_analytics(self) -> List[Dict]:
        """Fetch kibble analytics from view"""
        query = "SELECT * FROM v_kibble_analytics"
        return self.execute_query(query) or []
    
    def get_cat_health_summary(self) -> List[Dict]:
        """Fetch cat health summaries"""
        query = "SELECT * FROM v_cat_health"
        return self.execute_query(query) or []
    
    def get_feeding_trends(self, days: int = 30) -> List[Dict]:
        """Get feeding trends for last N days"""
        query = "SELECT * FROM v_feeding_trends"
        return self.execute_query(query) or []
    
    def get_top_value_kibbles(self, limit: int = 10) -> List[Dict]:
        """Get top kibbles by protein-to-price ratio"""
        query = """
            SELECT brand_name, protein_pct, price_per_kg, rating,
                   protein_pct / NULLIF(price_per_kg, 0) as value_ratio
            FROM kibbles
            WHERE price_per_kg > 0
            ORDER BY value_ratio DESC
            LIMIT %s
        """
        return self.execute_query(query, (limit,)) or []
    
    # ==========================================
    # RATING CALCULATION
    # ==========================================
    
    def calculate_rating(
        self, 
        protein: float, 
        fat: float, 
        fiber: float,
        moisture: float = 10.0
    ) -> str:
        """
        Calculate kibble quality rating based on nutrition profile
        
        Args:
            protein: Crude protein percentage
            fat: Crude fat percentage
            fiber: Crude fiber percentage
            moisture: Moisture percentage (default 10% for dry kibble)
        Returns:
            Rating grade: 'A', 'B', 'C', 'D', or 'F'
        """
        score = 0
        
        # 🔥 NEW: Convert to Dry Matter Basis if wet food
        if moisture > 50:  # Wet food (>50% moisture)
            dry_matter = 100 - moisture
            protein = (protein / dry_matter) * 100
            fat = (fat / dry_matter) * 100
            fiber = (fiber / dry_matter) * 100
            print(f"🌊 WET FOOD DETECTED! Converting to dry matter basis:")
            print(f"   Protein: {protein:.1f}% (dry matter)")
            print(f"   Fat: {fat:.1f}% (dry matter)")

        # Protein scoring (cats are obligate carnivores - high protein is critical)
        if protein >= 35:
            score += 40
        elif protein >= 30:
            score += 30
        elif protein >= 25:
            score += 20
        elif protein >= 20:
            score += 10
        
        # Fat scoring (12-18% is ideal for cats)
        if 12 <= fat <= 18:
            score += 30
        elif 10 <= fat < 12 or 18 < fat <= 20:
            score += 20
        elif 8 <= fat < 10 or 20 < fat <= 22:
            score += 10
        
        # Fiber scoring (3-6% is optimal)
        if 3 <= fiber <= 6:
            score += 30
        elif 2 <= fiber < 3 or 6 < fiber <= 8:
            score += 20
        elif fiber < 2 or fiber > 8:
            score += 10
        
        # Convert score to letter grade
        if score >= 80:
            return 'A'
        elif score >= 65:
            return 'B'
        elif score >= 50:
            return 'C'
        elif score >= 35:
            return 'D'
        else:
            return 'F'
    
    # ==========================================
    # USER-SPECIFIC OPERATIONS (OPTION A)
    # ==========================================

    def get_cats_by_user(self, user_id: str) -> List[Dict]:
        """Get cats for specific user"""
        query = """
            SELECT * FROM cats 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """
        return self.execute_query(query, (user_id,)) or []

    def get_kibbles_by_user(self, user_id: str) -> List[Dict]:
        """Get kibbles scanned by specific user"""
        query = """
            SELECT * FROM kibbles 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """
        return self.execute_query(query, (user_id,)) or []

    def get_scans_by_user(self, user_id: str) -> List[Dict]:
        """Get scan history for specific user"""
        query = """
            SELECT * FROM scan_history 
            WHERE user_id = %s 
            ORDER BY scanned_at DESC
        """
        return self.execute_query(query, (user_id,)) or []

    def get_feeding_logs_by_user(self, user_id: str) -> List[Dict]:
        """Get feeding logs for user's cats"""
        query = """
            SELECT fl.* FROM feeding_logs fl
            INNER JOIN cats c ON fl.cat_id = c.cat_id
            WHERE c.user_id = %s
            ORDER BY fl.fed_at DESC
        """
        return self.execute_query(query, (user_id,)) or []

    def add_cat(self, name, breed, age_years, age_months, weight_kg, gender, 
                activity_level, condition_score, health_conditions=None, bcs_numeric=None,
                user_id=None, user_name=None):
        """Add new cat to database with user tracking"""
        
        query = """
            INSERT INTO cats (
                name, breed, age_years, age_months, weight_kg, gender,
                activity_level, condition_score, health_conditions, bcs_numeric,
                user_id, user_name, created_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
            )
        """
        
        params = (
            name, breed, age_years, age_months, weight_kg, gender,
            activity_level, condition_score, health_conditions, bcs_numeric,
            user_id, user_name
        )
        
        return self.execute_update(query, params)

    def add_kibble(self, brand_name, product_name, protein_pct, fat_pct, 
                fiber_pct, moisture_pct=10.0, ash_pct=None, rating=None,
                price_per_kg=None, user_id=None, user_name=None):
        """Add new kibble to database with user tracking"""
        
        query = """
            INSERT INTO kibbles (
                brand_name, product_name, protein_pct, fat_pct, fiber_pct,
                moisture_pct, ash_pct, rating, price_per_kg,
                user_id, user_name, created_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
            )
        """
        
        params = (
            brand_name, product_name, protein_pct, fat_pct, fiber_pct,
            moisture_pct, ash_pct, rating, price_per_kg,
            user_id, user_name
        )
        
        return self.execute_update(query, params)

    def add_scan(self, user_id, user_name, kibble_data):
        """Add scan history record"""
        
        query = """
            INSERT INTO scan_history (
                user_id, user_name, brand_name, product_name,
                protein_pct, fat_pct, fiber_pct, rating,
                scanned_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, NOW()
            )
        """
        
        params = (
            user_id, user_name,
            kibble_data.get('brand_name'),
            kibble_data.get('product_name'),
            kibble_data.get('protein_pct'),
            kibble_data.get('fat_pct'),
            kibble_data.get('fiber_pct'),
            kibble_data.get('rating')
        )
        
        return self.execute_update(query, params)
    
    # ==========================================
    # UTILITY FUNCTIONS
    # ==========================================
    
    def health_check(self) -> bool:
        """
        Check database connectivity
        Returns: True if healthy, False otherwise
        """
        try:
            result = self.execute_query("SELECT 1 as health", fetch_one=True)
            return result is not None and result.get('health') == 1
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_table_stats(self) -> Dict[str, int]:
        """Get row counts for all tables"""
        tables = ['kibbles', 'cats', 'feeding_logs', 'nutrition_standards']
        stats = {}
        
        for table in tables:
            query = f"SELECT COUNT(*) as count FROM {table}"
            result = self.execute_query(query, fetch_one=True)
            stats[table] = result['count'] if result else 0
        
        return stats
    
    def backup_database(self, output_path: str) -> bool:
        """
        Create database backup (requires mysqldump in system PATH)
        
        Args:
            output_path: Path to save backup file
        
        Returns:
            True if successful
        """
        import subprocess
        
        try:
            cmd = [
                'mysqldump',
                '-h', Config.DB_HOST,
                '-P', str(Config.DB_PORT),
                '-u', Config.DB_USER,
                f'-p{Config.DB_PASSWORD}',
                Config.DB_NAME,
                '--result-file', output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"✅ Database backed up to {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Backup failed: {e}")
            return False
        except FileNotFoundError:
            logger.error("❌ mysqldump not found in system PATH")
            return False


# Singleton instance
try:
    print("🔄 Attempting database connection...")
    db_instance = Database()
    print("✅ Database connected successfully!")
except Exception as e:
    print(f"⚠️ Database connection failed: {e}")
    print("⚠️ App will continue in demo mode without database")
    db_instance = None


