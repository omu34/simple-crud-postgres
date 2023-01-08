import psycopg2
import psycopg2.extras

conn = psycopg2.connect(
    host="localhost",
    database="items",
    user='postgres',
    password='5599emoyo')

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS item1;')
cur.execute('CREATE TABLE item2 (id serial PRIMARY KEY,'
            'name VARCHAR(50) NOT NULL,'
            'bacode VARCHAR(50) NOT NULL,'
            'price INT NOT NULL,'
            'description VARCHAR(50) NOT NULL,'
            )
cur.execute('INSERT INTO item2 (name, bacode, price,description)'
            'VALUES (%s, %s, %s ,%s)',
            ('Nokia', '1000', 3000, 'A great smart phone!')
            )
cur.execute('INSERT INTO item2 (name, bacode, price, description)'
            'VALUES (%s, %s, %s, %s)',
            ('Samsung', '2000', 5000, 'Another great Iphone!')
            )

conn.commit()
cur.close()
conn.close()
