import tweepy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# classification dict
categories = {
    'social media': ['social', 'tik tok', 'facebook', 'twitter', 'tech', 'technology'],
    'gun violence': ['assault rifle', 'handgun', 'gun', 'shooting', 'shooter', 'armed'],
    'politics': ['politics', 'government', 'election', 'democracy'],
}

def classify_tweet(text):
    # tweet text vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([text])
    
    # naive bayes classifier
    clf = MultinomialNB()
    clf.fit(X, [0])
    
    # category prediction
    max_prob = -1
    category = None
    for cat, keywords in categories.items():
        prob = 0
        for keyword in keywords:
            if keyword in text.lower():
                prob += 1
        prob /= len(keywords)
        if prob > max_prob:
            max_prob = prob
            category = cat
    if max_prob < 0.5:
        category = 'other'
    return category

def print_tweet_subject(tweet):
    subject = classify_tweet(tweet.text)
    print(f'Tweet: {tweet.text}')
    print(f'Subject: {subject}\n')


query = 'something'
tweets = api.search_tweets(query, count=10)
for tweet in tweets:
    print_tweet_subject(tweet)
