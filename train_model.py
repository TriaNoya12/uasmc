import json
import pickle
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ==============================
# LOAD DATASET
# ==============================
with open("dataset.json", encoding="utf-8") as f:
    data = json.load(f)

texts = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        texts.append(pattern.lower())
        labels.append(intent["tag"])

# ==============================
# ANALISIS DATASET
# ==============================
intents = data["intents"]
num_intents = len(intents)
patterns_per_intent = {intent['tag']: len(intent['patterns']) for intent in intents}
total_patterns = sum(patterns_per_intent.values())

print("===== ANALISIS DATASET =====")
print(f"Jumlah intents: {num_intents}")
print(f"Total patterns: {total_patterns}")
print("Jumlah pattern per intent:")
for tag, count in patterns_per_intent.items():
    print(f"- {tag}: {count} pattern")

# ==============================
# TRAIN MODEL
# ==============================
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

# ==============================
# EVALUASI MODEL
# ==============================
y_pred = model.predict(X)
accuracy = np.mean(y_pred == labels)
print("\n===== EVALUASI MODEL =====")
print(f"Accuracy pada dataset training: {accuracy*100:.2f}%")

# Akurasi per intent
correct_per_intent = Counter()
total_per_intent = Counter()

for label, pred in zip(labels, y_pred):
    total_per_intent[label] += 1
    if label == pred:
        correct_per_intent[label] += 1

print("\nAkurasi per intent:")
for tag in total_per_intent:
    acc_intent = correct_per_intent[tag] / total_per_intent[tag] * 100
    print(f"- {tag}: {acc_intent:.2f}%")

# ==============================
# REKOMENDASI PERBAIKAN
# ==============================
print("\n===== REKOMENDASI PERBAIKAN =====")
print("- Tambahkan lebih banyak variasi pattern pada intent dengan akurasi rendah.")
print("- Pastikan dataset tidak bias ke intent tertentu agar chatbot lebih seimbang.")
print("- Pertimbangkan augmentasi data atau sinonim untuk memperkaya pertanyaan pengguna.")
print("- Bisa gunakan model lain atau hyperparameter tuning untuk meningkatkan performa.")

# ==============================
# SIMPAN MODEL & VECTORIZER
# ==============================
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\n✅ Training selesai! model.pkl & vectorizer.pkl berhasil dibuat")
