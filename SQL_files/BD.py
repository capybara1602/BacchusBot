import psycopg2 as ps
from config_data.config import Config, load_config
from environs import Env 

env = Env()
env.read_env(None)


def create_conection():
    password = env('PASSWORD')
    connection = ps.connect(dbname='sm_app', user='postgres', password=password, host='localhost')
    return connection



def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    
    cursor.execute(query)



def execute_read_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

connection = create_conection()

create_wine_table = """
    CREATE TABLE IF NOT EXISTS wine(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price TEXT,
        country TEXT,
        color TEXT,
        sugar TEXT,
        link TEXT

    )
    """

delete_wine = "DROP TABLE wine"

output_wine = "SELECT name, price, country, color, sugar, link FROM wine"



