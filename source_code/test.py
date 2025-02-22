from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Load data
df = pd.read_csv("../data/haunted_places.tsv", sep="\t")

# Preprocess text (Convert to lowercase)
df["cleaned_description"] = df["description"].str.lower()

# Use TF-IDF to extract important words
vectorizer = TfidfVectorizer(max_features=100, stop_words="english")  # Extracts top 100 keywords
tfidf_matrix = vectorizer.fit_transform(df["cleaned_description"])

# Get important keywords
important_keywords = vectorizer.get_feature_names_out()

# Print extracted keywords
print("🔹 Most Important Keywords:")
print(important_keywords)

#############################################################
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    """Extract named entities like apparition types and event descriptions."""
    if pd.isna(text):
        return "Unknown"

    doc = nlp(text.lower())
    entities = [ent.text for ent in doc.ents if ent.label_ in ["NORP", "PERSON", "EVENT"]]

    return entities if entities else "Unknown"


# Apply NER extraction
df["Entities"] = df["description"].apply(extract_entities)

# Display extracted entities
print(df[["description", "Entities"]].head(10))

###################################################################################
from gensim import corpora, models
import nltk
from nltk.tokenize import word_tokenize
import string

# Tokenize descriptions
df["tokens"] = df["cleaned_description"].apply(lambda x: word_tokenize(x) if pd.notna(x) else [])

# Remove stopwords & punctuation
stopwords = nltk.corpus.stopwords.words("english")
df["tokens"] = df["tokens"].apply(lambda x: [word for word in x if word not in stopwords and word not in string.punctuation])

# Create dictionary & corpus for LDA
dictionary = corpora.Dictionary(df["tokens"])
corpus = [dictionary.doc2bow(text) for text in df["tokens"]]

# Train LDA model with 5 topics
lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

# Print topics
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(f"Topic {topic[0]}: {topic[1]}")
