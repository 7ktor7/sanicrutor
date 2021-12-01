# ./models.py
import asyncio
import asyncpg
import datetime

async def myconn():
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect('postgresql://bjbvafbeszwvqk:14bb331a2e746694108dc37064e958a0c209da8569dfa9b3dd36c5f36ce65af8@ec2-3-217-91-165.compute-1.amazonaws.com/d38vvdankg655o')
    #conn = await asyncpg.connect(user='monty', password='qwerty8mM,./l',host='payk.pp.ua', port='5432', ssl=False,database='mydb77')
    # Execute a statement to create a new table.
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS rutor(
            id serial PRIMARY KEY,
            title text,
            seeds text,
            peers text,
            magnet text,
            created text,
            updated text,
            info_hash text,
            size text

        )
    ''')




    return conn

