import spacy
from gensim.models import KeyedVectors
from transformers import T5Tokenizer, T5ForConditionalGeneration



print("Loading spaCy...")
nlp = spacy.load("en_core_web_sm")

print("Loading Word2Vec...")
w2v = KeyedVectors.load_word2vec_format(
    "data/GoogleNews-vectors-negative300.bin",
    binary=True,
    limit=200000
)

print("Loading T5...")
MODEL_PATH = "data/final-model"
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

