from typing import Optional
from pydantic import BaseModel
from datetime import date
# Schéma de réponse pour le Département
class DepartementBase(BaseModel):
    nom: str
    localisation: str
    description: str
    contact: str
    est_interne: bool

class DepartementCreate(DepartementBase):
    pass

class Departement(DepartementBase):
    id: int

  
# Schéma de réponse pour le Service
class ServiceBase(BaseModel):
    nom: str
    localisation: Optional[str] = None
    contact: Optional[str] = None
    departement_id: Optional[int]  # Foreign key vers Departement

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int

   
# Schéma de réponse pour la Personne
class PersonneBase(BaseModel):
    nom: str
    prenom: str
    date_de_naissance: Optional[date] = None
    fonction: str
    photo: str
    service_id: int  # Foreign key vers Service

class PersonneCreate(PersonneBase):
    pass

class Personne(PersonneBase):
    id: int

    

# Schéma de réponse pour le TypeContact
class TypeContactBase(BaseModel):
    libelle: str
    description: Optional[str] = None

class TypeContactCreate(TypeContactBase):
    pass

class TypeContact(TypeContactBase):
    id: int

    

# Schéma de réponse pour le Contact
class ContactBase(BaseModel):
    valeur: str
    est_public: Optional[bool] = None
    personne_id: Optional[int]  # Foreign key vers Personne
    type_contact_id: Optional[int]  # Foreign key vers TypeContact
    service_id: Optional[int]  # Foreign key vers Service

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

# Schéma de réponse pour la gestion de système de rôle c'est à dire admin ou user

class UserBase(BaseModel):
    id: int  # ID de l'utilisateur dans la base de données
    username: str  # Nom d'utilisateur
    role: str  # Rôle de l'utilisateur (Agent ou Admin)

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
     
   


   
