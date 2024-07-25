import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load the dataset
df = pd.read_csv('furniture_data.csv')
descriptions = df['Description'].fillna('unknown')

# Preprocessing function
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)

# Apply preprocessing to the descriptions
descriptions = descriptions.apply(preprocess_text)

# Vectorize the descriptions
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = vectorizer.fit_transform(descriptions)

# Apply LDA
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X)

# Function to extract top words for each topic
def get_top_words(lda_model, vectorizer, n_words=10):
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-n_words:]]
        topics.append((topic_idx, top_words))
    return topics

# Extract and display top words for each topic
topics = get_top_words(lda, vectorizer)
for topic_idx, top_words in topics:
    print(f"Topic #{topic_idx + 1}: {', '.join(top_words)}")

# Define a mapping from topic numbers to style labels
topic_style_mapping = {
    0: 'Modern',
    1: 'Traditional',
    2: 'Rustic',
    3: 'Industrial',
    4: 'Contemporary'
}

# Predict the topic distribution for each description
topic_distribution = lda.transform(X)

# Assign the most dominant topic
dominant_topic = np.argmax(topic_distribution, axis=1)

# Convert numpy array to pandas Series for mapping
dominant_topic_series = pd.Series(dominant_topic)

# Map topics to styles
df['Style'] = dominant_topic_series.map(topic_style_mapping)

# Display the DataFrame with the assigned styles
print(df[['Description', 'Style']].head())

# Optional: Save the DataFrame with styles to a new CSV
df.to_csv('furniture_data_with_styles.csv', index=False)
