import json
import tweepy
import time
import requests
from pprint import pprint
with open("credentials.json") as f:
    credentials = json.load(f)
last_id = 1300000000000000000
twitter_name = "Bitc0inBar0n"

auth = tweepy.OAuthHandler(credentials["API_KEY"], credentials["API_SECRET"])
auth.set_access_token(credentials["ACCESS_TOKEN"], credentials["ACCESS_SECRET"])
api = tweepy.API(auth)

def alert_via_discord(user:str, crypto:str, full_tweet:str) -> None:
    hook = "https://discord.com/api/webhooks/812677344790577212/qbQZjSbbXLY9UyXHRZVUGaR2VAQYQyDGshglDzmnvHFr8VdwVXP5Rdb6QDVkJnTKKKPO"
    requests.post(hook, data={"content":f"{user} tweeted about {crypto}\nFull tweet: {full_tweet}", "username":"twitter_to_discord"})

cryptos_to_check = ["bitcoin", "ethereum","dogecoin","polkadot"]
tweets = []
users_to_monitor = ["Bitc0inBar0n","elonmusk"]
while 1:
    for user in users_to_monitor:
        tweets = api.user_timeline(screen_name = user,
                                count = 1,
                                include_rts = False,
                                tweet_mode='extended',
                                since_id = last_id
                                )
        for i in tweets:
            if i.id > last_id:
                print("New tweet : ", i.full_text)
                last_id = i.id
                for j in cryptos_to_check:
                    if j in i.full_text.lower(): 
                        alert_via_discord(user, j, i.full_text)
    print("sleeping")
    time.sleep(10)