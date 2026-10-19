import os
import mysql.connector 

def get_connection():
    host = os.getenv("MYSQL_HOST")
    if host:
        return mysql.connector.connect(
            host=host,
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jobnex"),
            connection_timeout=3
        )

    try:
        return mysql.connector.connect (
            host = "127.0.0.1",
            port = '3306',
            user = 'root',
            password = 'Algonex@2003',
            database = 'jobnex',
            connection_timeout = 3
        )
    except mysql.connector.Error:
        return mysql.connector.connect (
            host = "127.0.0.1",
            port = '3306',
            user = 'root',
            password = 'Algonex@123',
            database = 'jobnex',
            connection_timeout = 3
        )