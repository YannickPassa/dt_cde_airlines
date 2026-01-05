import logging
import json

from config import CLIENT_ID, CLIENT_SECRET
from api_client import token_access, request_FranceTravail
from log import setup_logging

setup_logging()

logging.info(CLIENT_ID)

def main():
    
    logging.info("Lancement de l'application")
    # Utilise les identifiants définis dans config.py
    token = token_access(CLIENT_ID, CLIENT_SECRET)
    if token:
        logging.info("Token obtenu : %s", token)
    else:
        logging.error("Échec de la récupération du token.")
        logging.error(CLIENT_ID)
   

    response = request_AirFranceKLM(CLIENT_ID,token)
    
    formatted_json = json.dumps(response.json(), indent=4)
    logging.info("Réponse complète de l'API :\n%s", formatted_json)
    
    if response is not None:
        if response.status_code == 200 | 206:
            response_json = response.json()  # Affiche la réponse JSON
            logging.info(response.json())
        else:
            logging.error(response.status_code)
 
    data= response.json()
    offers_list = data["resultats"]
  
#On s'assure de lancer main() depuis le main.
if __name__ == '__main__':
    main()
