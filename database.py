import psycopg2
from psycopg2 import sql

# Connexion à la base de données
def get_connection():
    return psycopg2.connect(
        dbname="Gestion_Contact", 
        user="Mon_utilisateur", 
        password="kramo", 
        host="localhost",  # db est le nom du service PostgreSQL dans votre docker-compose
        port="5432"
    )

# Fonction pour obtenir un curseur de base de données
def get_cursor():
    connection = get_connection()
    cursor = connection.cursor()
    return cursor, connection

# Fonction pour fermer la connexion
def close_connection(cursor, connection):
    cursor.close()
    connection.close()
