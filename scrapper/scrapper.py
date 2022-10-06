from selenium import webdriver
import warnings

warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("start-maximized")
options.add_argument("--log-level=3")
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
from logs.logs_config import main
import logging
from typing import List

url = "https://immobilier.lefigaro.fr/"
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()
driver.get(url)



class Scrapper:

    def __init__(self):
        pass

    def check_connect(self):
        main()
        # Trouver un moyen plus élégant de vérifier la connexion
        if "Saisissez une ou plusieurs villes" in driver.page_source:
            logging.info("La connexion à la page d'acceuil a bien réussie")

    #Trouver un moyen d'accepter les cookies
    def accept_cookie(self):

        #On accepte les cookies s'il y en a

        try:
            buttons = driver.find_elements("xpath",".//form//input[@type='button']")
            for h in buttons:
                print(h.text())
            #cookie_button = driver.find_element("xpath",('//<tagName>[contains(text(),"Continuer")]'))
            #driver.execute_script("arguments[0].click();", cookie_button)
            #logging.info("La page a demandé d'accepter les cookies, ce qui a été accepté")
        except:
            buttons = driver.find_elements("xpath",".//form//input[@type='button']")
            for h in buttons:
                print(h.text())

    def search_type(self, choice):
        driver.save_screenshot('screenshot_cookie.png')
        self.accept_cookie()
        choice = str(choice).lower()
        assert choice in [
            "acheter",
            "louer",
        ], "L'utilisateur doit choisir entre acheter et louer un bien"
        logging.warning(f"L'utilisateur a choisi l'otion {choice}")

        if driver.current_url!=url:
            driver.get(url)

        if choice == "acheter":
            driver.save_screenshot('screenshot1.png')
            element = driver.find_element("xpath",
                '//*[@id="homepage-v2"]/section[1]/div/div[1]/button[1]'
            )
            driver.execute_script("arguments[0].click();", element)

        else:
            
            element = driver.find_element("xpath",
                '//*[@id="homepage-v2"]/section[1]/div/div[1]/button[2]'
            )
            driver.execute_script("arguments[0].click();", element)

        search_button = driver.find_element("xpath",
            '//*[@id="homepage-v2"]/section[1]/div/button[2]'
        )
        driver.execute_script("arguments[0].click();", search_button)
        driver.implicitly_wait(1)
        
        self.accept_cookie()
        driver.implicitly_wait(1)
        
        if "Créer une alerte" in driver.page_source:
            logging.info("La recherche a bien aboutie")
        else:
            logging.info("La recherche n'a pas aboutie")

    def filter_search(self,ville:List):
        #Faire en sorte que l'utilisateur puisse entrer une liste de ville
        if len(ville)==1:
            logging.warning(f"L'utilisateur a choisi la région {ville[0]}".replace("[","").replace("]",""))
        else:
            logging.warning(f"L'utilisateur a choisi les régions: {[v for v in ville]}".replace("[","").replace("]",""))

        localisation_button=driver.find_element("xpath",'//*[@id="search-engine"]/div/div[1]/div[2]/div/span/span')
        driver.execute_script("arguments[0].click();", localisation_button)
        
        for choice_region in ville:

            driver.find_element("xpath","//*[@id='search-engine']/div/div[1]/div[2]/div[2]/div[2]/div/div/input").send_keys(choice_region)
            driver.implicitly_wait(3)
            first_choice=driver.find_element("xpath","//*[@id='search-engine']/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]")
            driver.execute_script("arguments[0].click();", first_choice)
        result_filter=driver.find_element("xpath",'//*[@id="bloc-list-classifieds"]').text
        print(result_filter)
        if len(ville)==1:
            if all([x.lower() in result_filter.lower() for x in ville]):
                logging.info(f"Le filtrage opéré sur la région de {ville[0]} a bien fonctionné".replace("[","").replace("]","")) 
        else:
            if all([x.lower() in result_filter.lower() for x in ville]):
                logging.info(f"Le filtrage opéré sur les régions de {[x for x in ville]} a bien fonctionné".replace("[","").replace("]","")) 
        driver.save_screenshot("screenshot_ville.png")