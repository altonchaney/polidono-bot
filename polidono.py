import sys
import tweepy
import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = tweepy.API(auth)

# classification dict
categories = {
  'social media': {
    'naicsCode': 511,
    'keywords': ['social', 'tik tok', 'facebook', 'twitter', 'tech', 'technology']
  },
  'gun violence': {
    'naicsCode': 332,
    'keywords': ['assault rifle', 'handgun', 'gun', 'shooting', 'shooter', 'armed']
  },
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
  for name, data in categories.items():
    prob = 0
    for keyword in data['keywords']:
      if keyword in text.lower():
        prob += 1
    prob /= len(data['keywords'])
    if prob > max_prob:
      max_prob = prob
      category = name
  if max_prob < 0.5:
    category = 'other'
  return category

def print_tweet_subject(tweet):
  subject = classify_tweet(tweet.text)
  print(f'Tweet: {tweet.text}')
  print(f'Subject: {subject}\n')

# List of politicians
politicians = {
  'Joe Biden': {
    'crpId': 'N00001669',
    'accounts': ['POTUS', 'JoeBiden']
  }
}

for politician, data in politicians.items():
  tweets = []
  for username in data['accounts']:
    tweets.append(twitterApi.user_timeline(screen_name=username, count=3))
  for tweet in tweets:
    print_tweet_subject(tweet)

    
    

    

    

# if certain subject is detected, find relevant political donations for companies / groups related to that industry
  try:
    
    openSecretsResponse = requests.get(f"https://www.opensecrets.org/api/?method=candIndByInd&cid={data['crpId']}&ind=K02&apikey={os.environ.get('OPEN_SECRETS_API_KEY')}").json()

    # then we'll check if we're even getting any valid data back so we don't clear out any existing data
    if 'data' in openSecretsResponse:
      twitterStatus = ''
      # generate tweet content
      try:
        print()
        
        # tweet generator (if too long we'll auto break it up)
        if twitterStatus != '':
          if len(twitterStatus) < 200:
            print(twitterStatus)
            try:
              # reply to detected tweet
              twitterApi.update_status(twitterStatus)
            except tweepy.TweepyException as e:
              print('Error updating status for ' + politician + ':')
              print(e)
              pass
          else:
            donoList = twitterStatus.split('\n')
            currentStatus = donoList[0]
            for dono in donoList:
              if len(currentStatus + '\n' + dono) < 200 and dono is not donoList[len(donoList) - 1]:
                if dono is not donoList[0]:
                  currentStatus += '\n' + dono
              else:
                if dono is donoList[len(donoList) - 1]:
                  currentStatus += '\n' + dono
                print(currentStatus)
                try:
                  # reply to detected tweet
                  twitterApi.update_status(currentStatus)
                except tweepy.TweepyException as e:
                  print('Error updating status for ' + politician + ':')
                  print(e)
                  pass
                currentStatus = donoList[0] + '\n' + dono
      except ValueError as e:
        print('JSON file error:')
        print(e)
        pass

    else:
      print('No JSON data')
      print('Feed Data:')
      print(openSecretsResponse)
      sys.exit(1)

  # if API errors out for any reason
  except requests.exceptions.RequestException as e:
    print('Request Error:')
    print(e)
    sys.exit(1)