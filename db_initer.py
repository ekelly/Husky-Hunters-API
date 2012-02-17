import psycopg2
from huskyhunter import DATABASE_URL

if __name__ == "__main__":
  connection = psycopg2.connect(host=DATABASE_URL.hostname, database=DATABASE_URL.path[1:],
                                user=DATABASE_URL.username, password=DATABASE_URL.password)
  cursor = connection.cursor()
  cursor.execute(open("scripts/huskyhunter-base.sql").read())
  connection.commit()
  cursor.close()
  connection.close()
