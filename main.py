from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Form, HTTPException 
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictCursor
from models import Departement, Service, Personne, TypeContact, Contact, User
from schemas import DepartementCreate, ServiceCreate, PersonneCreate, TypeContactCreate, ContactCreate, UserCreate
from datetime import date
from fastapi.responses import JSONResponse
import os
import psycopg2
from typing import Optional
# Initialisation de l'application FastAPI
app = FastAPI()

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (modifiez pour production)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes
)
# Fonction pour établir la connexion à la base de données

DB_NAME = "Gestion_Contact"
DB_USER = "Mon_utilisateur"
DB_PASSWORD = "kramo"
DB_HOST = "db" 
DB_PORT = "5432"

def get_db_connection():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,  
            user=DB_USER,
            password=DB_PASSWORD
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à la base de données : {str(e)}")


# endpoint pour tester la connexion à la base de données
@app.get("/test-db-connection")
def test_db_connection():
    try:
        conn = get_db_connection()
        conn.close()
        return {"message": "Connexion à la base de données réussie !"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à la base de données : {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion de contacts !"}

# ----------------- Gestion des départements ----------------
# end point pour pouvoir ajouter un département

@app.post("/departements/") 
def add_departement(departement: DepartementCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Departement (nom, localisation, description, contact, est_interne)
            VALUES (%s, %s, %s, %s, %s) RETURNING id, nom, localisation, description, contact, est_interne;
        """, (departement.nom, departement.localisation, departement.description, departement.contact, departement.est_interne))
        new_departement = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "message": "Département créé avec succès !",
            "departement": {
                "id": new_departement[0],
                "nom": new_departement[1],
                "localisation": new_departement[2],
                "description": new_departement[3],
                "contact": new_departement[4],
                "est_interne": new_departement[5],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création du département : {str(e)}")

# end point pour pouvoir récuperer tout les départements existants

@app.get("/departements/")  
def get_departements():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Departement")
        departements = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"message": "Départements récupérés avec succès !", "departements": departements}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la récupération des départements : {str(e)}")

# Endpoint pour rechercher un département par son nom
@app.get("/departements/{departement_nom}")
def search_departement(departement_nom: str , departement:DepartementCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Departement WHERE nom ILIKE %s", (f"%{departement_nom}%",))
        departements = cursor.fetchall()
        cursor.close()
        conn.close()

        if not departements:
            raise HTTPException(status_code=404, detail="Aucun département trouvé avec ce nom.")

        return {"message": "Département(s) trouvé(s) avec succès !", "departements": departements}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la recherche : {str(e)}")    
    
# end point pour pouvoir mettre à jour un département à partir de l'id

@app.put("/departements/{departement_id}") 
def update_departement(departement_id: int, departement: DepartementCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Departement
            SET nom = %s, localisation = %s, description = %s, contact = %s, est_interne = %s
            WHERE id = %s
            RETURNING id, nom, localisation, description, contact, est_interne;
        """, (departement.nom, departement.localisation, departement.description, departement.contact, departement.est_interne, departement_id))
        updated_departement = cursor.fetchone()
        if not updated_departement:
            raise HTTPException(status_code=404, detail="Département introuvable.")
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "message": "Département mis à jour avec succès !",
            "departement": {
                "id": updated_departement[0],
                "nom": updated_departement[1],
                "localisation": updated_departement[2],
                "description": updated_departement[3],
                "contact": updated_departement[4],
                "est_interne": updated_departement[5],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour du département : {str(e)}")
    
# end point pour pouvoir supprimer un département existant à partir de l'id

@app.delete("/departements/{departement_id}") 
def delete_departement(departement_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Departement WHERE id = %s RETURNING id;", (departement_id,))
        deleted_departement = cursor.fetchone()
        if not deleted_departement:
            raise HTTPException(status_code=404, detail="Département introuvable.")
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Département supprimé avec succès !", "departement_id": deleted_departement[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression du département : {str(e)}")

# ----------------- Gestion des services -----------------

# ----------------- ajout services -----------------

@app.post("/services/")
def add_service(service: ServiceCreate):
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Service (nom, localisation, contact, departement_id)
            VALUES (%s, %s, %s, %s) RETURNING id, nom, localisation, contact, departement_id;
        """, (service.nom, service.localisation, service.contact, service.departement_id))
        new_service = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "message": "Service créé avec succès !",
            "service": {
                "id": new_service[0],
                "nom": new_service[1],
                "localisation": new_service[2],
                "contact": new_service[3],
                "departement_id": new_service[4],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création du service : {str(e)}")

# -----------------  Endpoint pour récupérer tous les services -----------------
@app.get("/services/")
def get_services():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT Service.id, Service.nom, Service.localisation, Service.contact, Departement.nom AS departement_nom
            FROM Service
            LEFT JOIN Departement ON Service.departement_id = Departement.id
        """
        cursor.execute(query)
        services = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"message": "Services récupérés avec succès !", "services": services}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la récupération des services : {str(e)}")

# -----------------  Endpoint pour récupérer tous les services avec les personnes associées -----------------

@app.get("/services/{service_nom}")
def get_service_par_nom(service_nom: str):
    """
    Endpoint pour accéder aux informations d'un service et des personnes associées à partir du nom du service.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            s.id AS service_id,
            s.nom AS service_nom,
            s.localisation AS service_localisation,
            p.nom AS personne_nom,
            p.prenom AS personne_prenom,
            p.date_de_naissance AS date_de_naissance_personne,
            p.fonction AS fonction_personne
        FROM 
            service s
        LEFT JOIN 
            personne p ON p.service_id = s.id
        WHERE 
            s.nom = %s;
        """
        cursor.execute(query, (service_nom,))
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="Aucun service trouvé avec ce nom.")

        service_data = {
            "service_id": results[0][0],
            "service_nom": results[0][1],
            "service_localisation": results[0][2],
            "personnes": []
        }

        for row in results:
            if row[3]:  # Vérifie si une personne est associée
                personne_data = {
                    "personne_nom": row[3],
                    "personne_prenom": row[4],
                    "date_de_naissance_personne": row[5],
                    "fonction_personne": row[6],
                }
                service_data["personnes"].append(personne_data)

        cursor.close()
        conn.close()
        return service_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la recherche du service : {str(e)}")
        
# ----------------- mise à jour services -----------------

@app.put("/services/{service_id}")
def update_service(service_id: int, service: ServiceCreate):
    """
    Endpoint pour mettre à jour un service existant.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Service
            SET nom = %s, localisation = %s, contact = %s, departement_id = %s
            WHERE id = %s
            RETURNING id, nom, localisation, contact, departement_id;
        """, (service.nom, service.localisation, service.contact, service.departement_id, service_id))
        updated_service = cursor.fetchone()
        if not updated_service:
            raise HTTPException(status_code=404, detail="Service introuvable.")
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "message": "Service mis à jour avec succès !",
            "service": {
                "id": updated_service[0],
                "nom": updated_service[1],
                "localisation": updated_service[2],
                "contact": updated_service[3],
                "departement_id": updated_service[4],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour du service : {str(e)}")

# ----------------- suppression services -----------------

@app.delete("/services/{service_id}")
def delete_service(service_id: int):
    """
    Endpoint pour supprimer un service.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Service WHERE id = %s RETURNING id;", (service_id,))
        deleted_service = cursor.fetchone()
        if not deleted_service:
            raise HTTPException(status_code=404, detail="Service introuvable.")
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Service supprimé avec succès !", "service_id": deleted_service[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression du service : {str(e)}")
    

#-------pour récuperer les informations d’un service à partir du nom de ce service et les personnes associées----------------


# ----------------- Gestion des personnes -----------------
#endpoint pour ajouter une personne
@app.post("/personnes/")
def add_personne(
    nom: str = Form(...),
    prenom: str = Form(...),
    date_de_naissance: str = Form(...),
    fonction: str = Form(...),
    service_id: int = Form(...),
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insérer dans la base de données
        cursor.execute(
            """
            INSERT INTO Personne (nom, prenom, date_de_naissance, fonction, service_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, nom, prenom, date_de_naissance, fonction, service_id;
            """,
            (nom, prenom, date_de_naissance, fonction, service_id),
        )

        new_personne = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Personne créée avec succès !",
            "personne": {
                "id": new_personne[0],
                "nom": new_personne[1],
                "prenom": new_personne[2],
                "date_de_naissance": new_personne[3],
                "fonction": new_personne[4],
                "service_id": new_personne[5],
            },
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur : {str(e)}")

    
#------------pour récuperer la liste de toutes les personnes  

#Endpoint pour récupérer toutes les personnes.

@app.get("/personnes/")
def get_personnes():
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT p.id, p.nom, p.prenom, p.date_de_naissance, p.fonction, s.nom as service_nom 
            FROM Personne p 
            JOIN Service s ON p.service_id = s.id
        """)
        personnes = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"message": "Personnes récupérées avec succès !", "personnes": personnes}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la récupération des personnes : {str(e)}")
    
#-----------------------Endpoint pour rechercher les contacts associés à une personne à partir de son nom

@app.get("/personnes/{nom_personne}/contacts")
def get_contacts_par_nom_personne(nom_personne: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            c.id AS contact_id,
            c.valeur AS contact_valeur,
            tc.libelle AS type_contact_libelle,
            tc.description AS type_contact_description,
            c.est_public AS est_public,
            p.nom AS nom_personne,
            p.prenom AS prenom_personne,
            p.date_de_naissance AS date_de_naissance_personne,
            p.fonction AS fonction_personne,
            s.nom AS nom_service,
            s.localisation AS localisation_service
        FROM 
            contact c
        JOIN 
            personne p ON c.personne_id = p.id
        JOIN 
            typecontact tc ON c.type_contact_id = tc.id
        JOIN 
            service s ON c.service_id = s.id
        WHERE 
            p.nom = %s;
        """
        cursor.execute(query, (nom_personne,))
        result = cursor.fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="Aucun contact trouvé pour cette personne.")

        contacts_info = []
        for row in result:
            contact_data = {
                "contact_id": row[0],
                "contact_valeur": row[1],
                "type_contact_libelle": row[2],
                "type_contact_description": row[3],
                "est_public": row[4],
                "nom_personne": row[5],
                "prenom_personne": row[6],
                "date_de_naissance_personne": row[7],
                "fonction_personne": row[8],
                "nom_service": row[10],
                "localisation_service": row[11],
                "nom_departement": row[12],
                "localisation_departement": row[13],
                "departement_contact": row[14],
                "departement_est_interne": row[15],
            }
            contacts_info.append(contact_data)

        cursor.close()
        conn.close()
        return contacts_info

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la recherche des contacts : {str(e)}")

#-------------------pour mettre à jour-------------------------------
@app.put("/personnes/{personne_id}")
def update_personne(personne_id: int, personne: PersonneCreate):
    """
    Endpoint pour mettre à jour une personne existante.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Personne
            SET nom = %s, prenom = %s, date_de_naissance = %s, fonction = %s, service_id = %s
            WHERE id = %s
            RETURNING id, nom, prenom, date_de_naissance, fonction,service_id;
        """, (personne.nom, personne.prenom, personne.date_de_naissance, personne.fonction,personne.service_id, personne_id))
        updated_personne = cursor.fetchone()
        if not updated_personne:
            raise HTTPException(status_code=404, detail="Personne introuvable.")
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "message": "Personne mise à jour avec succès !",
            "personne": {
                "id": updated_personne[0],
                "nom": updated_personne[1],
                "prenom": updated_personne[2],
                "date_de_naissance": updated_personne[3],
                "fonction": updated_personne[4],
                "service_id": updated_personne[5],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour de la personne : {str(e)}")


@app.delete("/personnes/{personne_id}")
def delete_personne(personne_id: int):
    """
    Endpoint pour supprimer une personne.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Personne WHERE id = %s RETURNING id;", (personne_id,))
        deleted_personne = cursor.fetchone()
        if not deleted_personne:
            raise HTTPException(status_code=404, detail="Personne introuvable.")
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Personne supprimée avec succès !", "personne_id": deleted_personne[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression de la personne : {str(e)}")


# ----------------- Gestion contact -----------------
#------------Endpoint pour ajouter un contact
@app.post("/contacts/")
def add_contact(contact: ContactCreate):
    try:
        # Vérifiez que le service_id n'est pas null
        if contact.service_id is None:
            raise HTTPException(status_code=400, detail="Le champ 'service_id' ne peut pas être null.")

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Exécution de la requête d'insertion
        cursor.execute("""
            INSERT INTO Contact (valeur, est_public, personne_id, type_contact_id, service_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, valeur, est_public, personne_id, type_contact_id, service_id;
        """, (contact.valeur, contact.est_public, contact.personne_id, contact.type_contact_id, contact.service_id))

        # Récupération du contact inséré
        new_contact = cursor.fetchone()
        conn.commit()

        return {
            "message": "Contact créé avec succès !",
            "contact": {
                "id": new_contact[0],
                "valeur": new_contact[1],
                "est_public": new_contact[2],
                "personne_id": new_contact[3],
                "type_contact_id": new_contact[4],
                "service_id": new_contact[5],
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de création de contact : {str(e)}")
    
    finally:
        cursor.close()
        conn.close()


# Endpoint pour récupérer tous les contacts
@app.get("/contacts/")
def get_contacts():
    """
    Endpoint pour récupérer tous les contacts et leurs informations associées.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                c.id AS contact_id,
                c.valeur AS contact_valeur,
                tc.libelle AS type_contact_libelle,
                tc.description AS type_contact_description,
                c.est_public AS est_public,
                p.nom AS nom_personne,
                p.prenom AS prenom_personne,
                p.date_de_naissance AS date_de_naissance_personne,
                p.fonction AS fonction_personne,
                s.nom AS nom_service,
                s.localisation AS localisation_service,
                d.nom AS nom_departement,
                d.localisation AS localisation_departement,
                d.contact AS departement_contact,
                d.est_interne AS departement_est_interne
            FROM 
                contact c
            JOIN 
                personne p ON c.personne_id = p.id
            JOIN 
                typecontact tc ON c.type_contact_id = tc.id
            JOIN 
                service s ON c.service_id = s.id
            JOIN 
                departement d ON s.departement_id = d.id
        """)
        contacts = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"message": "Contacts récupérés avec succès !", "contacts": contacts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la récupération des contacts : {str(e)}")


# Endpoint pour recuperer tous les contacts associés à partir d'une valeur de contact

@app.get("/contacts/{valeur_contact}/contacts")
def get_contacts_par_valeur(valeur_contact: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            c.id AS contact_id,
            c.valeur AS contact_valeur,
            tc.libelle AS type_contact_libelle,
            tc.description AS type_contact_description,
            c.est_public AS est_public,
            p.nom AS nom_personne,
            p.prenom AS prenom_personne,
            p.date_de_naissance AS date_de_naissance_personne,
            p.fonction AS fonction_personne,
            s.nom AS nom_service,
            s.localisation AS localisation_service,
            d.nom AS nom_departement,
            d.localisation AS localisation_departement,
            d.contact AS departement_contact,
            d.est_interne AS departement_est_interne
        FROM 
            contact c
        JOIN 
            personne p ON c.personne_id = p.id
        JOIN 
            typecontact tc ON c.type_contact_id = tc.id
        JOIN 
            service s ON c.service_id = s.id
        JOIN 
            departement d ON s.departement_id = d.id
        WHERE 
            c.valeur = %s;
        """
        cursor.execute(query, (valeur_contact,))
        result = cursor.fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="Aucun contact trouvé pour cette valeur.")

        contacts_info = []
        for row in result:
            contact_data = {
                "contact_id": row[0],
                "contact_valeur": row[1],
                "type_contact_libelle": row[2],
                "type_contact_description": row[3],
                "est_public": row[4],
                "nom_personne": row[5],
                "prenom_personne": row[6],
                "date_de_naissance_personne": row[7],
                "fonction_personne": row[8],
                "nom_service": row[9],
                "localisation_service": row[10],
                "nom_departement": row[11],
                "localisation_departement": row[12],
                "departement_contact": row[13],
                "departement_est_interne": row[14],
            }
            contacts_info.append(contact_data)

        cursor.close()
        conn.close()
        return contacts_info

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la recherche des contacts : {str(e)}")

# Endpoint pour recuperer tous les contacts à partir de l'id

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):
    """
    Endpoint pour récupérer un contact spécifique par son ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                c.id AS contact_id,
                c.valeur AS contact_valeur,
                c.est_public AS est_public,
                c.personne_id AS personne_id,
                c.type_contact_id AS type_contact_id,
                c.service_id AS service_id
            FROM 
                contact c
            WHERE 
                c.id = %s
        """, (contact_id,))
        contact = cursor.fetchone()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact introuvable.")
        cursor.close()
        conn.close()
        return {"message": "Contact récupéré avec succès !", "contact": contact}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la récupération du contact : {str(e)}")

# Mise à jour des informations du contact à partir de l'id

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: dict):
    """
    Endpoint pour mettre à jour un contact existant.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            UPDATE contact
            SET valeur = %s, type_contact_id = %s, est_public = %s, personne_id = %s, service_id = %s
            WHERE id = %s
            RETURNING id, valeur, type_contact_id, est_public, personne_id, service_id;
        """, (
            contact["valeur"],
            contact["type_contact_id"],
            contact["est_public"],
            contact["personne_id"],
            contact["service_id"],
            contact_id
        ))
        
        updated_contact = cursor.fetchone()
        if not updated_contact:
            raise HTTPException(status_code=404, detail="Contact introuvable.")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "message": "Contact mis à jour avec succès !",
            "contact": updated_contact
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour du contact : {str(e)}")


#pour mettre à jour à partir de la valeur contact

@app.put("/contacts/{contact_valeur}")
def update_contact(contact_valeur: str, updated_contact: dict):
    """
    Endpoint pour mettre à jour un contact existant à partir de sa valeur.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Requête de mise à jour
        cursor.execute("""
            UPDATE contact
            SET valeur = %s, type_contact_id = %s, est_public = %s, personne_id = %s, service_id = %s
            WHERE valeur = %s
            RETURNING id, valeur, type_contact_id, est_public, personne_id, service_id;
        """, (
            updated_contact.get("valeur"),
            updated_contact.get("type_contact_id"),
            updated_contact.get("est_public"),
            updated_contact.get("personne_id"),
            updated_contact.get("service_id"),
            contact_valeur
        ))

        # Récupération du contact mis à jour
        contact = cursor.fetchone()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact introuvable.")
        
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Contact mis à jour avec succès !",
            "contact": {
                "id": contact[0],
                "valeur": contact[1],
                "type_contact_id": contact[2],
                "est_public": contact[3],
                "personne_id": contact[4],
                "service_id": contact[5],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour du contact : {str(e)}")


##pour commpter les éléments de la bd

@app.get("/statistiques")
def get_statistiques():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer le nombre de départements
        cursor.execute("SELECT COUNT(*) FROM departement;")
        nb_departements = cursor.fetchone()[0]

        # Récupérer le nombre de services
        cursor.execute("SELECT COUNT(*) FROM service;")
        nb_services = cursor.fetchone()[0]

        # Récupérer le nombre de personnes
        cursor.execute("SELECT COUNT(*) FROM personne;")
        nb_personnes = cursor.fetchone()[0]

        # Récupérer le nombre de conatcts
        cursor.execute("SELECT COUNT (*) FROM contact;")
        nb_contacts = cursor.fetchone()[0]


        # Fermer la connexion
        cursor.close()
        conn.close()

        return {
            "departements": nb_departements,
            "services": nb_services,
            "personnes": nb_personnes,
            "contacts":nb_contacts
        }

    except Exception as e:
        return {"error": str(e)}

""" en fin de compte les endpoints ci-dessus permettront de :
"""
