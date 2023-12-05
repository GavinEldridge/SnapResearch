import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Load CSV file into a DataFrame

df = pd.read_csv("povertyfinance_comm.csv")

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Download NLTK resources (stopwords and punkt tokenizer)
# Uncomment the following two lines if you haven't downloaded them before
# import nltk
# nltk.download(['stopwords', 'punkt'])

# Get English stop words
stop_words = set(stopwords.words('english'))

# Function to preprocess text (remove stop words, lowercase)
def preprocess_text(text):
    # Check for NaN values
    if pd.isna(text):
        return ""
    
    # Tokenize the text
    words = word_tokenize(text)
    
    # Remove stop words and punctuation, convert to lowercase
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    
    # Join the words back into a string
    return ' '.join(filtered_words)

# Apply preprocessing to the 'text' column
df['processed_text'] = df['Comment Text'].apply(preprocess_text)

# Function to get sentiment score
def get_sentiment_score(text):
    return sia.polarity_scores(text)['compound']

# Create new columns 'sentiment_score' and 'sentiment' after each line
df['sentiment_score'] = df['processed_text'].apply(get_sentiment_score)
df['sentiment'] = df['sentiment_score'].apply(lambda score: 'Positive' if score >= 0.05 else ('Negative' if score <= -0.05 else 'Neutral'))

# Print the DataFrame with sentiment scores and labels
print(df[['Comment Text', 'processed_text', 'sentiment_score', 'sentiment']])
print(df[0:5])
