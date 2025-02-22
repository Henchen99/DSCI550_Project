import pandas as pd
import os
import re
import spacy
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora, models
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK resources are available
nltk.download("stopwords")
nltk.download("punkt")

##################################################
####### Load and Preprocess Haunted Places #######
##################################################

# Define file paths
input_file = os.path.join("..", "data", "haunted_places.tsv")
output_file = os.path.join("..", "data", "haunted_places_enriched.tsv")

# Check if the file exists
if not os.path.exists(input_file):
    print(f"\u274C Error: File not found at {os.path.abspath(input_file)}")
    exit(1)

# Load TSV file
df = pd.read_csv(input_file, sep="\t")
print(f"\u2705 Loaded dataset: {input_file}")

##################################################
############### Feature Engineering ##############
##################################################

# Preprocess text (Tokenization, Lowercasing, Removing Stopwords & Punctuation)
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])  # Remove punctuation
    tokens = word_tokenize(text)
    return " ".join([word for word in tokens if word not in stop_words])  # Remove stopwords

# Apply text preprocessing
df["cleaned_description"] = df["description"].apply(preprocess_text)

# Use TF-IDF to identify important keywords
vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["cleaned_description"])
important_keywords = vectorizer.get_feature_names_out()

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    if pd.isna(text):
        return "Unknown"
    doc = nlp(text.lower())
    entities = [ent.text for ent in doc.ents if ent.label_ in ["NORP", "PERSON", "EVENT", "ORG"]]
    return entities if entities else "Unknown"

df["Entities"] = df["description"].apply(extract_entities)

# Tokenize descriptions
df["tokens"] = df["cleaned_description"].apply(lambda x: word_tokenize(x) if pd.notna(x) else [])

# Remove stopwords & punctuation
df["tokens"] = df["tokens"].apply(lambda x: [word for word in x if word not in stopwords and word not in string.punctuation])

# Create dictionary & corpus for LDA
dictionary = corpora.Dictionary(df["tokens"])
corpus = [dictionary.doc2bow(text) for text in df["tokens"]]

# Train LDA model with 5 topics
lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(f"Topic {topic[0]}: {topic[1]}")

# Train Word2Vec model on descriptions
word2vec_model = Word2Vec(sentences=df["tokens"], vector_size=50, window=5, min_count=1, workers=4)

# Save the enriched dataset
df.to_csv(output_file, sep="\t", index=False)
print(f"\u2705 Feature engineering completed! Enriched dataset saved at: {output_file}")
