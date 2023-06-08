import csv
import re
import nltk
import os
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')

def preprocess(text):
    text = re.sub(r'\W', ' ', text.lower())
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

def load_data(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append((preprocess(row[0]), row[1]))
    return data

def find_best_match(question, data, threshold=0.5):
    vectorizer = TfidfVectorizer()
    questions = [q for q, _ in data]
    questions.append(preprocess(question))
    tfidf_matrix = vectorizer.fit_transform(questions)
    similarity_scores = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])
    best_match_index = similarity_scores.argmax()
    best_match_score = similarity_scores[0, best_match_index]

    if best_match_score < threshold:
        return None

    return data[best_match_index][1]

def execute(request, ray):
    output = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'science.csv')
    data = load_data(file_path)

    for text in request['text']:
        user_question = text
        if user_question.lower() in ['quit', 'exit', 'bye']:
            response = "Chatbot: Goodbye!"
        else:
            answer = find_best_match(user_question, data)
            if answer is None:
                response = "Chatbot: I'm sorry, I don't know the answer to that question."
            else:
                response = f"Chatbot: {answer}"
            response += "\nDo you have any further questions? (Type 'quit' to exit)"
        output.append(response)

    return {'text': output}
def chatbot():
    print("Hello! I'm a science chatbot. Ask me any science-related question!")
    while True:
        user_question = input("You: ")
        if user_question.lower() in ['quit', 'exit', 'bye']:
            print("Chatbot: Goodbye!")
            break

        response = execute({'text': [user_question]}, None)
        print(response['text'][0])

if __name__ == "__main__":
    chatbot()