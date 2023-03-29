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
    
    # for each item in the classification dict, adjust probability of specific category if that text is found in the tweet text
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

# get ONLY tweets in the last X minutes from specified users
users = ['alamoAlerts_003', 'alamoAlerts_004']
for user in users:  
    tweets = api.user_timeline(screen_name='alamoAlerts_003', count=3)
    for tweet in tweets:
        print_tweet_subject(tweet)

        # if certain subject is detected, find relevant political donations for companies / groups related to that

        # generate tweet content

        # reply to detected tweet
