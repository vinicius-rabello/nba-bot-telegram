import psycopg2
from config.settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, SSLMODE

def get_connection():
    """Create and return a database connection"""
    DB_CONFIG = {
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
        "sslmode": SSLMODE
    }
    return psycopg2.connect(**DB_CONFIG)

def get_by_date(date):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Construct the SQL query
        select_query = f"""
        SELECT * FROM games
        WHERE full_date = %s 
        """
        
        # Execute the query
        cursor.execute(select_query, (date,))
        results = cursor.fetchall()
        return results
        
    except Exception as e:
        # Log the error
        print(f"Database error: {e}")
        return None
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()