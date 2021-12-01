# ./models.py
import asyncio
import psycopg2
import datetime

def myconnmy():
    
    conn =  psycopg2.connect('dbname=d38vvdankg655o user=bjbvafbeszwvqk password=14bb331a2e746694108dc37064e958a0c209da8569dfa9b3dd36c5f36ce65af8 host=ec2-3-217-91-165.compute-1.amazonaws.com')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS rutor(
            id serial PRIMARY KEY,
            title text,
            url text,
            seeds text,
            peers text,
            magnet text,
            created text,
            updated text,
            info_hash text,
            size text)
    ''')
    #conn.commit()
    print("table created")



    return conn

