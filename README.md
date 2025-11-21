# dt_cde_airlines
Repo git utilisé dans le cadre du projet cde airlines de la formation data engineer de datascientest

## Environnement & Installation

### Exigences du système

Pour lancer ce projet sur votre machine locale vous devez [installer Docker](https://docs.docker.com/engine/install/).


### Votre environnement virtuel Python

`uv` est utilisé pour installer la bonne version de Python et les dépendances
du projet.

Pour l’installer, suivre la documentation officielle
https://docs.astral.sh/uv/getting-started/installation/. Un paquet est
disponible pour la plupart des distributions Linux.

    make venv
    source .venv/bin/activate

### Le logiciel [direnv](https://direnv.net)

Sans oublier d'installer les [hooks](https://direnv.net/docs/hook.html) ni de
lancer `direnv allow` ensuite dans ce répertoire.
[Tuto](https://stackoverflow.com/questions/49083789/how-to-add-new-line-in-bashrc-file-in-ubuntu) pour ajouter une nouvelle ligne sur le fichier `bashrc` (linux) ou `.bash_profile` (mac OS)

Créer un fichier `.envrc.local` contenant au minimum le chemin vers le .venv : `echo "source .venv/bin/activate" >> .envrc.local`

### Votre fichier ``.env``

Le fichier `env.example` contient des valeurs par défaut directement utilisables,
sauf pour le chargement des dumps du Pilotage en production.

Il sert de modèle pour la création de votre propre fichier `.env`; n'hésitez pas
à le modifier si votre configuration locale (adresse, nom, port de votre base de
données...) est différente.

    cp env.example .env
    # modifiez le ficher `.env` si besoin
    # Une fois les variables d'environnement chargées vérifiez que vous disposez bien de `psql`

Notez que le fichier commité `.env-base` contient les bonnes variables d'environnement
quel que soit votre environnement de développement et n'est pas censé être "personnalisé".

## Docker

La base de données (PostgreSQL) et Airflow peuvent tous être lancés ensemble avec

    docker compose up --build

## DBT et base de données 

Pour vérifier que DBT est bien configuré :

    dbt debug
