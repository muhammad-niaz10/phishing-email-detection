import joblib
import shap
from fastapi import FastAPI
from pydantic import BaseModel
from prepocess import clean,remove_stopwords,apply_spacy_lemmitization

app = FastAPI()

model = joblib.load("phishing_rf_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")
explainer = shap.TreeExplainer(model)


class EmailInput(BaseModel):
    text: str


@app.post("/predict")
def predict(data: EmailInput):

    cleaned_text = clean(data.text)
    cleaned_text = remove_stopwords(cleaned_text)
    cleaned_text = apply_spacy_lemmitization(cleaned_text)


    X_vec = vectorizer.transform([cleaned_text]).toarray()

    phishing_prob = model.predict_proba(X_vec)[0][1]
    threshold = 0.50
    pred = 1 if phishing_prob >= threshold else 0

    shap_vals = explainer(X_vec)
    phishing_scores = shap_vals.values[0, :, 1]

    words = vectorizer.get_feature_names_out()

    reasons = {}
    for i in range(len(words)):
        if X_vec[0][i] > 0:
            reasons[words[i]] = round(float(phishing_scores[i]), 4)

    return {
        "prediction": "Phishing" if pred == 1 else "Safe",
        "confidence": round(float(phishing_prob), 4),
        "word_impact_scores": reasons,
    }