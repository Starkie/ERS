import tweepy

API_KEY = ""
API_SECRET= ""

ACCESS_TOKEN  = ""
ACCESS_TOKEN_SECRET = ''

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

query = 'ETSINF'
max_tweets = 2
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

#type Status Tweepy
for st in searched_tweets:
 print("The status was created at : " + str(st.created_at))
 print("The text is : " + st.text)
