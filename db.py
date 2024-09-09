import psycopg2
from config import load_config

def get_db_connection():
    """Establishes and returns a PostgreSQL database connection using the configuration."""
    db_config = load_config()

    # Create a connection using psycopg2
    conn = psycopg2.connect(
        host=db_config["host"],
        user=db_config["username"],
        password=db_config["password"],
        dbname=db_config["dbname"],
        port=db_config["port"]
    )
    
    return conn
