from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch 

# Charger le modèle SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def read_questions_in_batches(file_path, batch_size=20):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    batches = []
    for i in range(0, len(lines), batch_size):
        batch = lines[i:i + batch_size]
        batch_string = ''.join(batch)
        batches.append(batch_string)

    return batches

def update_question_list(existing_questions, new_questions, threshold=0.75):
    # Encoder les questions existantes
    existing_embeddings = model.encode(existing_questions, convert_to_tensor=True)

    for question in new_questions:
        question_embedding = model.encode(question, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(question_embedding, existing_embeddings)

        # Trouver l'index de la question la plus similaire
        most_similar_idx = torch.argmax(similarities).item()
        highest_similarity = similarities[0][most_similar_idx].item()

        if highest_similarity < threshold:
            # Si la similarité est au-dessus du seuil, incrémenter le compteur
            # existing_questions[most_similar_idx] += " (x{})".format(int(existing_questions[most_similar_idx].split('(x')[-1][0]) + 1)
        # else:
            # Sinon, ajouter la nouvelle question
            existing_questions.append(question)
        else:
            print ("simi")

    return existing_questions

# Exemple d'utilisation
file_path = 'questions_entretien.txt'
batches_of_questions = read_questions_in_batches(file_path)

# Initialiser la liste des questions avec le premier lot
existing_questions = batches_of_questions[0].splitlines()

# Mettre à jour la liste des questions avec les lots suivants
for i in range(1, len(batches_of_questions)):
    print(i)
    new_questions = batches_of_questions[i].splitlines()
    existing_questions = update_question_list(existing_questions, new_questions)

# Afficher les questions mises à jour
q = ""
for question in existing_questions:
    print(question)
    q+=question +'\n'

with open('questions_entretien_nettoyés_bert.txt', 'w', encoding='utf-8') as file:
    file.write(q)
