from typing import Optional
from pydantic import BaseModel
from datetime import date

# Modèle de base pour le Département
class Departement(BaseModel):
    id: Optional[int]  # La clé primaire peut être optionnelle car elle sera définie par la base de données
    nom: str
    localisation: Optional[str] = None
    description: Optional[str] = None
    contact: Optional[str] = None
    est_interne: Optional[bool] = None

    

# Modèle de base pour le Service
class Service(BaseModel):
    id: Optional[int]
    nom: str
    localisation: Optional[str] = None
    contact: Optional[str] = None
    departement_id: Optional[int]  # Foreign key vers Departement

    

# Modèle de base pour la Personne
class Personne(BaseModel):
    id: Optional[int]
    nom: str
    prenom: str
    date_de_naissance: Optional[date] = None
    fonction: Optional[str] = None
    photo: Optional[str] = None
   

# Modèle de base pour le TypeContact
class TypeContact(BaseModel):
    id: Optional[int]
    libelle: str
    description: Optional[str] = None



# Modèle de base pour le Contact
class Contact(BaseModel):
    id: Optional[int]
    valeur: str
    est_public: Optional[bool] = None
    personne_id: Optional[int]  # Clé etrangère vers Personne
    type_contact_id: Optional[int]  # Clé etrangère vers TypeContact
    service_id: Optional[int]  # Clé etrangère vers Service


# Modèle de base pour le User (qui est utilisé pour gérer le système de gestion des rôles)

class User(BaseModel):
    id: Optional[int]  
    username: str
    password: str  
    role: str  # Le rôle sera soit Agent, soit Admin , cest ce que j'ai defini dans ma table sql


