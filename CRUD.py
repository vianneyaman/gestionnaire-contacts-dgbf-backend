
import psycopg2
from psycopg2.extras import RealDictCursor
from database import get_cursor # Fonction pour obtenir le curseur de la base de données
from models import Departement, Service, Personne, TypeContact, Contact

# Connexion à la base de données 
def get_cursor():
    # Remplace les paramètres par les informations de ta base de données
    connection = psycopg2.connect(
        host="localhost",
        database="Gestion_Contact",
        user="Mon_utilisateur",
        password="kramo",
        port="5432"
    )
    return connection.cursor(cursor_factory=RealDictCursor)
try:
    conn = psycopg2.connect(
        dbname="Gestion_Contact", user="Mon_utilisateur", password="kramo", host="localhost"
    )
    print("Connexion réussie à la base de données")
except Exception as e:
    print("Erreur de connexion :", e)
    
# --- CRUD pour Departement ---
def create_departement(departement_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO departement (nom, localisation, description, contact, est_interne) 
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """,
                (departement_data['nom'], departement_data['localisation'], departement_data['description'], 
                 departement_data['contact'], departement_data['est_interne'])
            )
            departement_id = cursor.fetchone()[0]
        print(f"Département '{departement_data['nom']}' créé avec succès avec l'ID {departement_id}.")
        return departement_id
    except Exception as e:
        print(f"Erreur lors de la créatijyjyton du département : {e}")
        print(f"Type d'erreur : {type(e)}")  # Affiche le type de l'erreur
        return None

def get_departement(departement_id):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT id, nom, localisation, description, contact, est_interne FROM departement WHERE id = %s;",
                (departement_id,)
            )
            departement = cursor.fetchone()
            if departement is None:
                print(f"Aucun département trouvé avec l'ID {departement_id}.")
            else:
                return departement
    except Exception as e:
        print(f"Erreur lors de la récupération du département : {e}")
        print(f"Type d'erreur : {type(e)}")
        return None

def update_departement(departement_id, departement_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE departement 
                SET nom = %s, localisation = %s, description = %s, contact = %s, est_interne = %s 
                WHERE id = %s;
                """,
                (departement_data['nom'], departement_data['localisation'], departement_data['description'], 
                 departement_data['contact'], departement_data['est_interne'], departement_id)
            )
            if cursor.rowcount == 0:
                print(f"Aucun département trouvé avec l'ID {departement_id} à mettre à jour.")
            else:
                print(f"Département '{departement_data['nom']}' mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du département : {e}")
        print(f"Type d'erreur : {type(e)}")

def delete_departement(departement_id):
    try:
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM departement WHERE id = %s;", (departement_id,))
            if cursor.rowcount == 0:
                print(f"Aucun département trouvé avec l'ID {departement_id} à supprimer.")
            else:
                print(f"Département {departement_id} supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression du département : {e}")
        print(f"Type d'erreur : {type(e)}")

# --- CRUD pour Service ---
def create_service(service_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO service (nom, localisation, contact, departement_id) 
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (service_data['nom'], service_data['localisation'], service_data['contact'], service_data['departement_id'])
            )
            service_id = cursor.fetchone()[0]
        print(f"Service '{service_data['nom']}' créé avec succès avec l'ID {service_id}.")
        return service_id
    except Exception as e:
        print(f"Erreur lors de la création du service : {e}")
        print(f"Type d'erreur : {type(e)}")  # Affiche le type de l'erreur
        return None

def get_service(service_id):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT id, nom, localisation, contact, departement_id FROM service WHERE id = %s;",
                (service_id,)
            )
            service = cursor.fetchone()
            if service is None:
                print(f"Aucun service trouvé avec l'ID {service_id}.")
            else:
                return service
    except Exception as e:
        print(f"Erreur lors de la récupération du service : {e}")
        print(f"Type d'erreur : {type(e)}")
        return None

def update_service(service_id, service_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE service 
                SET nom = %s, localisation = %s, contact = %s, departement_id = %s 
                WHERE id = %s;
                """,
                (service_data['nom'], service_data['localisation'], service_data['contact'], service_data['departement_id'], service_id)
            )
            if cursor.rowcount == 0:
                print(f"Aucun service trouvé avec l'ID {service_id} à mettre à jour.")
            else:
                print(f"Service '{service_data['nom']}' mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du service : {e}")
        print(f"Type d'erreur : {type(e)}")

def delete_service(service_id):
    try:
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM service WHERE id = %s;", (service_id,))
            if cursor.rowcount == 0:
                print(f"Aucun service trouvé avec l'ID {service_id} à supprimer.")
            else:
                print(f"Service {service_id} supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression du service : {e}")
        print(f"Type d'erreur : {type(e)}")


# --- CRUD pour Personne ---
def create_personne(personne_data):
    try:
        # Vérification de la présence de la photo, en l'absence la valeur peut être None
        photo = personne_data.get('photo', None)
        with get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO personne (nom, prenom, date_de_naissance, fonction, photo, typecontact_id) 
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                """,
                (personne_data['nom'], personne_data['prenom'], personne_data['date_de_naissance'], 
                 personne_data.get('fonction', None), photo, personne_data['typecontact_id'])
            )
            personne_id = cursor.fetchone()[0]
        print(f"Personne '{personne_data['nom']} {personne_data['prenom']}' créée avec succès avec l'ID {personne_id}.")
        return personne_id
    except Exception as e:
        print(f"Erreur lors de la création de la personne : {e}")
        return None

def get_personne(personne_id):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nom, prenom, date_de_naissance, fonction, photo, typecontact_id 
                FROM personne 
                WHERE id = %s;
                """,
                (personne_id,)
            )
            personne = cursor.fetchone()
            if personne is None:
                print(f"Aucune personne trouvée avec l'ID {personne_id}.")
            else:
                return personne
    except Exception as e:
        print(f"Erreur lors de la récupération de la personne : {e}")
        return None

def update_personne(personne_id, personne_data):
    try:
        # Vérification si photo est fournie, sinon utiliser None
        photo = personne_data.get('photo', None)
        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE personne 
                SET nom = %s, prenom = %s, date_de_naissance = %s, fonction = %s, photo = %s, typecontact_id = %s 
                WHERE id = %s;
                """,
                (personne_data['nom'], personne_data['prenom'], personne_data['date_de_naissance'],
                 personne_data.get('fonction', None), photo, personne_data['typecontact_id'], personne_id)
            )
            if cursor.rowcount == 0:
                print(f"Aucune personne trouvée avec l'ID {personne_id} à mettre à jour.")
            else:
                print(f"Personne '{personne_data['nom']} {personne_data['prenom']}' mise à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la personne : {e}")

def delete_personne(personne_id):
    try:
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM personne WHERE id = %s;", (personne_id,))
            if cursor.rowcount == 0:
                print(f"Aucune personne trouvée avec l'ID {personne_id} à supprimer.")
            else:
                print(f"Personne {personne_id} supprimée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la personne : {e}")


# --- CRUD pour TypeContact ---
def create_type_contact(type_contact_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO TypeContact (libelle, description) VALUES (%s, %s) RETURNING id;",
                (type_contact_data['libelle'], type_contact_data.get('description', None))
            )
            type_contact_id = cursor.fetchone()[0]
        print(f"Type de contact '{type_contact_data['libelle']}' créé avec succès, ID : {type_contact_id}")
        return type_contact_id
    except Exception as e:
        print(f"Erreur lors de la création du type de contact : {e}")
        return None

def get_type_contact(type_contact_id):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT id, libelle, description FROM TypeContact WHERE id = %s;",
                (type_contact_id,)
            )
            type_contact = cursor.fetchone()
            if type_contact is None:
                print(f"Aucun type de contact trouvé avec l'ID {type_contact_id}.")
            else:
                return type_contact
    except Exception as e:
        print(f"Erreur lors de la récupération du type de contact : {e}")
        return None

def update_type_contact(type_contact_id, type_contact_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE TypeContact 
                SET libelle = %s, description = %s 
                WHERE id = %s;
                """,
                (type_contact_data['libelle'], type_contact_data.get('description', None), type_contact_id)
            )
            if cursor.rowcount == 0:
                print(f"Aucun type de contact trouvé avec l'ID {type_contact_id} à mettre à jour.")
            else:
                print(f"Type de contact '{type_contact_data['libelle']}' mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du type de contact : {e}")

def delete_type_contact(type_contact_id):
    try:
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM TypeContact WHERE id = %s;", (type_contact_id,))
            if cursor.rowcount == 0:
                print(f"Aucun type de contact trouvé avec l'ID {type_contact_id} à supprimer.")
            else:
                print(f"Type de contact {type_contact_id} supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression du type de contact : {e}")


# --- CRUD pour Contact ---
def create_contact(contact_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Contact (valeur, est_public, personne_id, type_contact_id, service_id) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (contact_data['valeur'], contact_data['est_public'], contact_data['personne_id'], 
                 contact_data['type_contact_id'], contact_data['service_id'])
            )
            contact_id = cursor.fetchone()[0]
        print(f"Contact créé avec succès avec l'ID {contact_id}.")
        return contact_id
    except Exception as e:
        print(f"Erreur lors de la création du contact : {e}")
        return None

def get_contact(contact_id):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT id, valeur, est_public, personne_id, type_contact_id, service_id FROM Contact WHERE id = %s;",
                (contact_id,)
            )
            contact = cursor.fetchone()
            if contact is None:
                print(f"Aucun contact trouvé avec l'ID {contact_id}.")
            else:
                return contact
    except Exception as e:
        print(f"Erreur lors de la récupération du contact : {e}")
        return None

def update_contact(contact_id, contact_data):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE Contact 
                SET valeur = %s, est_public = %s, personne_id = %s, type_contact_id = %s, service_id = %s 
                WHERE id = %s;
                """,
                (contact_data['valeur'], contact_data['est_public'], contact_data['personne_id'], 
                 contact_data['type_contact_id'], contact_data['service_id'], contact_id)
            )
            if cursor.rowcount == 0:
                print(f"Aucun contact trouvé avec l'ID {contact_id} à mettre à jour.")
            else:
                print(f"Contact avec l'ID {contact_id} mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du contact : {e}")

def delete_contact(contact_id):
    try:
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM Contact WHERE id = %s;", (contact_id,))
            if cursor.rowcount == 0:
                print(f"Aucun contact trouvé avec l'ID {contact_id} à supprimer.")
            else:
                print(f"Contact avec l'ID {contact_id} supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression du contact : {e}")
