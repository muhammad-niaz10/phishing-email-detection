import re
import nltk
from nltk.corpus import stopwords
import spacy

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

nlp = spacy.load("en_core_web_sm")



def clean(text):
  text=text.lower()
  text=re.sub(r"https?//\S+|www\.\S+","url",text)
  text=re.sub(r"[^a-zA-Z]"," ",text)
  return text


def remove_stopwords(text):
  words=text.split()
  filtered_words = [w for w in words if w not in stop_words]
  return " ".join(filtered_words)


def apply_spacy_lemmitization(text):
  words=nlp(text)
  return " ".join([token.lemma_ for token in words])