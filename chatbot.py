import json
import random
import pickle

# load model & vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ganti NAMA FILE sesuai dataset kamu
with open("dataset.json", encoding="utf-8") as f:
    intents = json.load(f)

def get_response(user_input):
    user_input = user_input.lower()

    X = vectorizer.transform([user_input])
    tag = model.predict(X)[0]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Maaf, saya belum memahami pertanyaan tersebut 🙏 Silakan tanyakan seputar KRS, KHS, UKT, fakultas, prodi, atau pendaftaran."
