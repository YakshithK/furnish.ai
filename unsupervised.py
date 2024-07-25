from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary
import pandas as pd
import pyLDAvis
import pyLDAvis.lda_model  # Updated import for LDA visualization
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required nltk data
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)

def main():
    # Load the dataset
    df = pd.read_csv('furniture_data.csv')

    # Handle missing values in the 'Description' column
    df['Description'] = df['Description'].fillna('unknown')

    # Apply preprocessing
    df['Description'] = df['Description'].apply(preprocess_text)

    # Vectorize the descriptions
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X = vectorizer.fit_transform(df['Description'])

    # Apply LDA
    lda = LatentDirichletAllocation(n_components=3, random_state=42, learning_method='online', doc_topic_prior=0.1, topic_word_prior=0.1)
    lda.fit(X)

    # Display LDA topics
    print("LDA Topics:")
    for index, topic in enumerate(lda.components_):
        print(f"Topic #{index + 1}:")
        print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])

    # Compute coherence score for LDA
    texts = [text.split() for text in df['Description']]
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_gensim = LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)
    coherence_model_lda = CoherenceModel(model=lda_gensim, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print(f'Coherence Score for LDA: {coherence_lda}')

    # Visualize LDA topics
    
    vis_lda = pyLDAvis.lda_model.prepare(lda, X, vectorizer)
    pyLDAvis.save_html(vis_lda, 'lda_visualization.html')

    # Apply NMF
    nmf = NMF(n_components=3, random_state=42)
    W = nmf.fit_transform(X)
    H = nmf.components_

    # Display NMF topics
    print("NMF Topics:")
    for index, topic in enumerate(H):
        print(f"Topic #{index + 1}:")
        print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])

    # Optional: Compute coherence score for NMF (not directly available in gensim)
    print("Coherence score is generally more suitable for LDA. NMF does not have a direct coherence score calculation.")

if __name__ == '__main__':
    main()
