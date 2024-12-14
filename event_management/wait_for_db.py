import os
import time
import psycopg2

def wait_for_db():
    while True:
        try:
            psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host='db'
            )
            break
        except psycopg2.OperationalError:
            print('Очікування бази даних...')
            time.sleep(1)

if __name__ == '__main__':
    wait_for_db() 