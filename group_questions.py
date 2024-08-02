import openai


Max_token = 2024

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

def read_questions_in_batches(file_path, batch_size=20):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    batches = []
    for i in range(0, len(lines), batch_size):
        batch = lines[i:i + batch_size]
        batch_string = ''.join(batch)
        batches.append(batch_string)

    return batches

# Exemple d'utilisation
file_path = 'questions_entretien_sqr.txt'
batches_of_questions = read_questions_in_batches(file_path)
print(len(batches_of_questions))

# Affichage des lots de questions
# for idx, batch in enumerate(batches_of_questions):
#     print(f"Batch {idx + 1}:")
#     for line in batch:
#         print(line.strip())
#     print("\n" + "="*50 + "\n")

print((batches_of_questions[2]))



liste_question = batches_of_questions[0]

    # Liste de témoignages
for i in range (1,len(batches_of_questions)-1):
    prompt = [
       {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": f"voici une liste de questions {liste_question}, je vais te donner une autre série de questions, si c'est une nouvelle question ajoute la à la liste, si c'est une question similaire à une des question de la lisgte alors ajoute un compteur au bout de la question pour savoir combien de fois elle est apparue. Aussi, reformule les question de manière synthétiques les questions qui sont adaptés. Les questions maths et les brains teasers doivent rester faisable si ils sont synthétisés. Garde seulement les questions de maths,brain teasers, ou exercice de code"
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "voici la liste des questions: " + batches_of_questions[i],
                }
            ]
            },
    ]
   
    
    def complete_response(prompt):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            temperature=1,
            max_tokens=Max_token,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
    
        return response.choices[0].message.content
   
    complete = False
    full_response = ""
    while not complete:
        response = complete_response(prompt)
        full_response += response
        if len(response) < Max_token:
            complete = True
        else:
            prompt = [
                {
                    "role": "system",
                    "content": "Continuez la réponse précédente."
                },
                {
                    "role": "user",
                    "content": ""
                }
            ]
    
    liste_question = full_response
    # liste_question = response.choices[0].message.content
    print(i)

print(liste_question)


# Enregistrement des questions dans un document texte
with open('questions_entretien_nettoyés_sqr.txt', 'w', encoding='utf-8') as file:
    file.write(liste_question)
