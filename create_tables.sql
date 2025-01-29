-- je vais commencer par créer département parce qu'il n'a pas de clé etrangère

-- Création de la table Departement
CREATE TABLE IF NOT EXISTS Departement (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    localisation VARCHAR(255) NOT NULL,
    "description" VARCHAR(255),
    contact VARCHAR(255),
    est_interne BOOLEAN NOT NULL
);



-- Après avoir créer département je vais créer service parce qu'à partir d'un service on doit pouvoir voir les éléments de la table département

-- Création de la table Service

CREATE TABLE IF NOT EXISTS Service (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    localisation VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    departement_id INT NOT NULL,
    CONSTRAINT fk_departement
        FOREIGN KEY (departement_id)
        REFERENCES Departement(id)
        ON DELETE CASCADE
);


-- je peux créer ensuite personne . personne fait référence à service

-- Création de la table Personne
CREATE TABLE IF NOT EXISTS Personne (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    date_de_naissance DATE,
    fonction VARCHAR(255),
    photo BYTEA,
    service_id INT NOT NULL,
    CONSTRAINT fk_service
        FOREIGN KEY (service_id)
        REFERENCES Service(id)
        ON DELETE CASCADE
);



-- je peux commencer par créer TypeContact parce qu'il n'a pas de clé etrangère

-- Création de la table TypeContact
CREATE TABLE IF NOT EXISTS TypeContact (
    id SERIAL PRIMARY KEY,
    libelle VARCHAR(255) NOT NULL,
    description TEXT
);


-- je finis par créer Contact parce qu'elle contient toutes les clés des autres tables donc 
-- c'est à partir d'ici que nous pourrions voir toutes les informations des autres autres 

-- Création de la table Contact

CREATE TABLE IF NOT EXISTS Contact (
    id SERIAL PRIMARY KEY,
    valeur VARCHAR(255) NOT NULL,
    est_public BOOLEAN NOT NULL,
    personne_id INT NOT NULL,
    type_contact_id INT NOT NULL,
    service_id INT NOT NULL,
    CONSTRAINT fk_personne
        FOREIGN KEY (personne_id)
        REFERENCES Personne(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_type_contact
        FOREIGN KEY (type_contact_id)
        REFERENCES TypeContact(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_service
        FOREIGN KEY (service_id)
        REFERENCES Service(id)
        ON DELETE CASCADE
);




