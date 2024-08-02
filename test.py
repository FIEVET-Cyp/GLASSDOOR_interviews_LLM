import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import openai

url = 'https://www.glassdoor.fr/Interview/Qube-Research-and-Technologies-Interview-Questions-E3226090.htm'  # Remplacer par l'URL réelle



def questions(url_glassdoor):
    # Chemin vers le ChromeDriver
    chrome_driver_path = 'C:/Users/33641/Desktop/Glassdoor/chromedriver-win64/chromedriver-win64/chromedriver.exe'

    # Initialisation du service ChromeDriver
    service = Service(executable_path=chrome_driver_path)

    # Initialisation du navigateur Chrome avec le service
    driver = webdriver.Chrome(service=service)

    # Accès à la page web
    url = url_glassdoor  # Remplacer par l'URL réelle
    driver.get(url)

    # Extraire le contenu du corps de la page
    body_text = driver.find_element(By.TAG_NAME, 'body').text

    # Extraire le texte après la phrase spécifiée
    start_phrase = "Notre priorité est de mériter votre confiance. Pour cette raison, les entreprises ne sont pas autorisées à modifier ou à supprimer les entretiens."
    start_index = body_text.find(start_phrase)

    if start_index != -1:
        body_text = body_text[start_index + len(start_phrase):]

    # Utiliser une expression régulière pour extraire les textes entre "Entretien" et "Répondre À La Question"
    pattern = re.compile(r'Entretien(.*?)Répondre À La Question', re.DOTALL)
    matches = pattern.findall(body_text)

    # Supprimer les sous-sections "Entretien" des correspondances
    cleaned_matches = [re.sub(r'Entretien.*?', '', match, flags=re.DOTALL).strip() for match in matches]

    def get_text(text):
        lignes = text.splitlines()
        bon_text = ""
        bon = False
        for ligne in lignes:
            print(len(ligne))
            if len(ligne) == 0:
                bon = True
            if bon == True:
                bon_text+=ligne
        return bon_text

    bon_texts = []
    for text in cleaned_matches:
        bon_texts.append(get_text(text))
    print(bon_texts)

    text_gpt  = ''
    for text in bon_texts:
        text_gpt+= "  "+ text



    # Fermer le navigateur
    driver.quit()

    # Remplacez par votre clé API OpenAI
    
    def read_api_keys(file_path):
        keys = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                name, value = line.strip().split('=')
                keys[name] = value
        return keys

    api_keys = read_api_keys('api_key.txt')

    openai.api_key = api_keys.get("OPENAI_API")


    # Liste de témoignages
    temoignages = bon_texts

    # client = OpenAI()
    response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "voici une liste de témoignage d'interviews, je veux que tu renvois la liste des questions qui ont été posé, seulement si elles ont un lien avec des brainteasers,maths ou ia "
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": text_gpt,
            }
        ]
        },
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    response_text = response.choices[0].message.content
    print(response_text)
    return response_text


def get_next_url(base_url, page_number):
    return f"{base_url}_P{page_number}.htm"

# Exemple d'utilisation
base_url = 'https://www.glassdoor.fr/Entretien/Two-Sigma-questions-entretien-d-embauche-E241045'
current_page = 0


# print(next_url)  # Devrait afficher 'https://www.glassdoor.fr/Entretien/Citadel-questions-entretien-d-embauche-E14937_P3.htm'

fini = False
all_questions = ""
while not fini:
    next_url = get_next_url(base_url, current_page + 1)
    current_page += 1
    if current_page == 62:
        fini = True
    questions_entretien = questions(next_url)
    all_questions += questions_entretien + "\n"

# Enregistrement des questions dans un document texte
with open('questions_entretien_2sig.txt', 'w', encoding='utf-8') as file:
    file.write(all_questions)