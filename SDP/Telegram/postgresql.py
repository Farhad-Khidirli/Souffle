import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="root"
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY NOT NULL,
        public_address VARCHAR(255),
        private_key VARCHAR(255),
        phone_number VARCHAR(20),
        email_address VARCHAR(255),
        balance DOUBLE PRECISION
    )
""")
conn.commit()


def insert_into(_id, _public_address, _private_key, _phone_number, _email_address, _balance):
    values = (_id, _public_address, _private_key, _phone_number, _email_address, _balance)

    cursor.execute("""
        INSERT INTO USERS (id, public_address, private_key, phone_number, email_address, balance)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, values)

    conn.commit()


def retrieve_by_id(_id):
    try:
        cursor.execute("SELECT * FROM USERS WHERE id = %s", (_id,))
        return cursor.fetchone(), True
    except:
        print("User with id {} doesn't exist.".format(_id))
        return None, False


def retrieve_all():
    cursor.execute("SELECT * FROM USERS")
    return cursor.fetchall()


def close_cursor():
    cursor.close()
    conn.close()
