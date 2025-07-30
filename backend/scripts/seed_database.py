import bcrypt
import psycopg2
import os
from typing import List, Tuple

###
# This script is used to seed the database with users
# This should be run after init.sql is run
#
###

def hash_password(password: str) -> str:
    # Hash and salt the password
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

def seed_users() -> List[Tuple[str, str]]:
    return [
        ("admin@test.com", "admin"),
        ("user@test.com", "password123!"),
        ("account@test.com", "P@ssw0rd"),
    ]


def main():
    # Database connection
    db_params = {
        'host': os.getenv("DB_HOST", "localhost"),
        'database': os.getenv("DB_NAME", "myapp"),
        'user': os.getenv("DB_USER", "postgres"),
        'password': os.getenv("DB_PASSWORD", "password123!"),
    }

    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        users = seed_users()

        for email, plain_password in users:
            hashed_password = hash_password(plain_password)

            insert_query = """
                INSERT INTO users (email,password)
                VALUES (%s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING id, email;
            """
        
            cur.execute(insert_query, (email, hashed_password))
            result = cur.fetchone()

            if result:
                print(f"Seeded user: {email}")
            else:
                print(f"Failed to seed user: {email}")

        conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.rollback()

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()