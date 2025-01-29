------script qui me permet de voir tout les contacts c'est à dire ce qui est après <AS> 
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
    p.photo AS photo_personne,
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
    departement d ON s.departement_id = d.id;


--------------------recherchez les contacts à partir du nom  ----
SELECT 
    c.id AS contact_id,
    c.valeur AS contact_valeur,
    tc.libelle AS type_contact_libelle,
    tc.description AS type_contact_description,
    c.est_public AS est_public,
    p.date_de_naissance AS date_de_naissance_personne,
    p.fonction AS fonction_personne,
    p.photo AS photo_personne,
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
    p.nom = 'nom recherché'
--------------------recherchez tout les contacts associés à partir du numéro ----
--------------------je vais faire ça apres avoir fais les endpoints de contacts
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
    p.photo AS photo_personne,
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
    c.valeur = 'ValeurContact';

-------------------- pour rechercher les informations d’un service à partir du nom de ce service et les personnes associées----------------
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
    s.nom = 'Service recherché'

    -------------------- pour rechercher les informations d’un service à partir du nom et les personnes associées au service----------------
