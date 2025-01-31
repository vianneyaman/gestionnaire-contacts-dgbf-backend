-- je vais commencer par créer département parce qu'il n'a pas de clé etrangère
2----
-- Création de la table Departement
CREATE TABLE IF NOT EXISTS Departement (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    localisation VARCHAR(255) NOT NULL,
    "description" VARCHAR(255),
    contact VARCHAR(255),
    est_interne BOOLEAN NOT NULL
);


3------
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
4----
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
1--------
-- Création de la table TypeContact
CREATE TABLE IF NOT EXISTS TypeContact (
    id SERIAL PRIMARY KEY,
    libelle VARCHAR(255) NOT NULL,
    description TEXT
);


-- je finis par créer Contact parce qu'elle contient toutes les clés des autres tables donc 
-- c'est à partir d'ici que nous pourrions voir toutes les informations des autres autres 
5-----
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
























-- 1. Table Département
INSERT INTO departement(id, nom, localisation, description, contact, est_interne) VALUES
(1000001, 'Département Marketing', 'Bureau principal', 'Responsable de la stratégie marketing', 'contact@marketing.com', true),
(1000002, 'Département Vente', 'Bureau secondaire', 'Responsable des ventes', 'contact@vente.com', true),
(1000003, 'Département RH', 'Bureau principal', 'Responsable des ressources humaines', 'contact@rh.com', true),
(1000004, 'Département Informatique', 'Bureau secondaire', 'Support et développement logiciel', 'contact@info.com', true),
(1000005, 'Département Finances', 'Bureau principal', 'Gestion financière et comptabilité', 'contact@finances.com', true),
(1000006, 'Département Juridique', 'Bureau principal', 'Conseil juridique interne', 'contact@juridique.com', true),
(1000007, 'Département Communication', 'Bureau secondaire', 'Communication interne et externe', 'contact@com.com', true),
(1000008, 'Département Logistique', 'Bureau principal', 'Gestion des stocks et approvisionnements', 'contact@logistique.com', true),
(1000009, 'Département Support Client', 'Bureau secondaire', 'Support et assistance aux clients', 'contact@support.com', true),
(1000010, 'Département Recherche et Développement', 'Bureau principal', 'Innovation et développement de nouveaux produits', 'contact@rd.com', true),
(1000011, 'Département Production', 'Bureau secondaire', 'Production des biens et services', 'contact@production.com', true),
(1000012, 'Département Qualité', 'Bureau principal', 'Contrôle qualité et conformité', 'contact@qualite.com', true),
(1000013, 'Département Informatique', 'Bureau principal', 'Infrastructure informatique', 'contact@infrastructure.com', false),
(1000014, 'Département Marketing Digital', 'Bureau secondaire', 'Publicité en ligne et SEO', 'contact@marketingdigital.com', false);

-- 2. Table Service
INSERT INTO service(id, nom, localisation, contact, departement_id) VALUES
(1000501, 'Service Financier', 'Abidjan', '0102345678', 1000005),
(1000502, 'RH Administration', 'Abidjan', 'contact@dgbf.ci', 1000003),
(1000503, 'Service Informatique', 'Yamoussoukro', '0123456789', 1000004),
(1000504, 'Développement logiciel', 'Abidjan', 'dev@dgbf.ci', 1000004),
(1000505, 'Sécurité Informatique', 'Abidjan', 'security@dgbf.ci', 1000006),
(1000506, 'Réseau', 'Abidjan', 'network@dgbf.ci', 1000007),
(1000507, 'Maintenance', 'Abidjan', 'maintenance@dgbf.ci', 1000008),
(1000508, 'Nettoyage', 'Abidjan', 'cleaning@dgbf.ci', 1000009),
(1000509, 'Vigiles', 'Abidjan', 'guards@dgbf.ci', 1000010),
(1000510, 'Logistique', 'Abidjan', 'logistics@dgbf.ci', 1000011),
(1000511, 'Communication', 'Abidjan', 'communication@dgbf.ci', 1000012),
(1000512, 'Marketing', 'Abidjan', 'marketing@dgbf.ci', 1000013),
(1000513, 'Juridique', 'Abidjan', 'legal@dgbf.ci', 1000014),
(1000514, 'Développement', 'Abidjan', 'dev@dgbf.ci', 1000004),
(1000515, 'Sécurité Informatique', 'Abidjan', 'secinfo@dgbf.ci', 1000006),
(1000516, 'Réseau', 'Abidjan', 'reseau@dgbf.ci', 1000007),
(1000517, 'Maintenance Informatique', 'Abidjan', 'maintenance@dgbf.ci', 1000008),
(1000518, 'Nettoyage', 'Abidjan', 'nettoyage@dgbf.ci', 1000009),
(1000519, 'Vigiles', 'Abidjan', 'vigiles@dgbf.ci', 1000010),
(1000520, 'Systèmes dInformation', 'Abidjan', 'it@dgbf.ci', 1000004),
(1000521, 'Gestion de Projet', 'Abidjan', 'projets@dgbf.ci', 1000011),
(1000522, 'Marketing', 'Abidjan', 'marketing@dgbf.ci', 1000012),
(1000523, 'Comptabilité', 'Abidjan', 'compta@dgbf.ci', 1000013),
(1000524, 'Logistique', 'Abidjan', 'logistique@dgbf.ci', 1000014);

-- 3. Table Type de Contact
INSERT INTO typecontact (id, libelle, description) VALUES
(10000001, 'Téléphone pro', 'Numéro professionnel'),
(10000002, 'Email pro', 'Adresse email professionnel'),
(10000003, 'Fax pro', 'Numéro de fax professionnel'),
(10000004, 'SMS pro', 'Messagetexte professionnel'),
(10000005, 'WhatsApp pro', 'WhatsApp professionnel'),
(10000006, 'Telegram pro', 'Telegram professionnel'),
(10000007, 'Skype pro', 'Skype professionnel'),
(10000008, 'LinkedIn pro', 'Profil LinkedIn professionnel'),
(10000009, 'Twitter pro', 'Compte Twitter professionnel'),
(10000010, 'Facebook pro', 'Compte Facebook professionnel'),
(10000011, 'Téléphone perso', 'Numéro personnel'),
(10000012, 'Email perso', 'Adresse email personnel'),
(10000013, 'SMS perso', 'Messagetexte personnel'),
(10000014, 'WhatsApp perso', 'WhatsApp personnel'),
(10000015, 'Facebook perso', 'Compte Facebook perso'),
(10000016, 'Adresse pro', 'Adresse de travail(bureau, siège)'),
(10000017, 'Adresse perso', 'Adresse personnelle(Domicile)');


-- 4. Table Personne
INSERT INTO personne (nom, prenom, date_de_naissance, fonction, service_id) VALUES
('Dupont', 'Alice', '1985-02-15', 'Responsable Financier', 1000501),
('Martin', 'Bernard', '1990-04-25', 'Assistante RH', 1000502),
('Durand', 'Claire', '1982-09-30', 'Développeuse', 1000503),
('Lemoine', 'David', '1991-01-10', 'Chef de projet', 1000504),
('Robert', 'Eva', '1986-07-22', 'Analyste Sécurité', 1000505),
('Garnier', 'François', '1983-11-02', 'Technicien Réseau', 1000506),
('Bouchard', 'Georges', '1994-12-13', 'Responsable Maintenance', 1000507),
('Vidal', 'Hélène', '1987-05-19', 'Responsable Nettoyage', 1000508),
('Perez', 'Isabelle', '1992-03-27', 'Chef de sécurité', 1000509),
('Rousseau', 'Jean', '1984-08-14', 'Responsable Logistique', 1000510),
('Laurent', 'Kévin', '1995-06-20', 'Responsable Communication', 1000511),
('Blanc', 'Lise', '1990-02-01', 'Chef de projet Marketing', 1000512),
('Giraud', 'Monique', '1980-11-04', 'Juriste', 1000513),
('Dubois', 'Nathalie', '1988-07-16', 'Chef Développement', 1000514),
('Fournier', 'Olivier', '1993-05-09', 'Analyste Réseau', 1000515),
('Lefevre', 'Patrick', '1981-01-28', 'Responsable Maintenance IT', 1000516),
('Meyer', 'Quentin', '1989-12-05', 'Responsable Projet', 1000517),
('Noël', 'Romain', '1992-11-13', 'Responsable Marketing', 1000518),
('Pires', 'Sophie', '1990-08-29', 'Comptable', 1000519),
('Lemoine', 'Thierry', '1986-03-03', 'Responsable Informatique', 1000520),
('Chavez', 'Valérie', '1994-05-21', 'Chef de Projet', 1000521),
('Benoit', 'Xavier', '1982-06-07', 'Directeur Marketing', 1000522),
('Dufresne', 'Yasmine', '1991-02-18', 'Technicien Réseau', 1000523),
('Vallée', 'Zara', '1983-04-12', 'Chef Sécurité Informatique', 1000524);

-- 5. Table contact
INSERT INTO contact (id, valeur, est_public, personne_id, type_contact_id, service_id) VALUES
(100001, '0102345678', true, 93, 10000001, 1000501),
(100002, 'contact@dgbf.ci', true, 94, 10000002, 1000502),
(100003, '0202345678', true, 95, 10000001, 1000503),
(100004, 'SMS: 0701234567', true, 96, 10000004, 1000504),
(100005, 'whatsapp: +2250102345678', true, 97, 10000005, 1000505),
(100006, 'telegram: @aminataY', true, 98, 10000006, 1000506),
(100007, 'skype: kouadio.d', true, 99, 10000007, 1000507),
(100008, 'linkedin: aminatayao', true, 100, 10000008, 1000508),
(100009, 'twitter: @tech_ami', true, 101, 10000009, 1000509),
(100010, 'facebook: Fatou Kouadio', true, 102, 10000010, 1000510),
(100011, '0123456789', true, 103, 10000011, 1000511),
(100012, 'mail: salimata.sidibe@dgbf.ci', true, 104, 10000012, 1000512),
(100013, 'sms: 0102345678', true, 105, 10000013, 1000513),
(100014, 'whatsapp: +2250701234567', true, 106, 10000014, 1000514),
(100015, 'facebook: @oussmanekita', true, 107, 10000015, 1000515),
(100016, 'adresse: 24 ruedesaffaires, Abidjan', true, 108, 10000016, 1000516),
(100017, 'adresse: 123 rue du commerce, Abidjan', true, 109, 10000017, 1000517),
(100018, '0101234567', true, 93, 10000001, 1000501),
(100019, 'alice.dupont@dgbf.ci', true, 93, 10000002, 1000501),
(100020, 'contact@bernardmartin.ci', true, 94, 10000002, 1000502),
(100021, 'sms: 0702345678', true, 95, 10000004, 1000503),
(100022, 'whatsapp: +2250123456789', true, 95, 10000005, 1000504),
(100023, 'telegram: @davidlemoine', true, 96, 10000006, 1000505),
(100024, 'skype: david.l', true, 96, 10000007, 1000506),
(100025, 'linkedin: eva.robert', true, 97, 10000008, 1000507),
(100026, 'twitter: @franckgarnier', true, 97, 10000009, 1000508),
(100027, 'facebook: @jeremybouchard', true, 98, 10000010, 1000509),
(100028, 'téléphone: 0103456789', true, 99, 10000011, 1000510);