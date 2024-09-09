import os
import yaml

def load_config():
    config_path = "config/config.yaml"
    
    # Load the YAML config file if it exists
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
    else:
        config = {}

    # Set precedence order: environment variables -> YAML config -> default values
    db_config = {
        "host": os.getenv("DB_HOST", config.get("database", {}).get("host", "localhost")),
        "username": os.getenv("DB_USER", config.get("database", {}).get("username", "default_user")),
        "password": os.getenv("DB_PASS", config.get("database", {}).get("password", "default_pass")),
        "dbname": os.getenv("DB_NAME", config.get("database", {}).get("dbname", "default_db")),
        "port": os.getenv("DB_PORT", config.get("database", {}).get("port", 5432))  # Default port 5432 for PostgreSQL
    }
    
    return db_config
