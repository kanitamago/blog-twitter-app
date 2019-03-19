import tweepy
from time import sleep
import sys

consumer_key = "StNpeQK6CoF5FpQbtcdkcZ5kT"
consumer_secret = "tOKFYnmzjoSZDt643rctWQxH5U5LGc5aucRkJQSp63nbfLbkLN"
access_token_key = "993720491431968768-lwUEGrp7WWUtVAYQyS9sTBMcmLeirBu"
access_token_secret = "zSpfPFZeo51BbbLIiURJGMXhuE1c1KeDizdqpeHhoKm38"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

class Create_api:
    API = None
    def __init__(self):
        global API
        print("Create Twitter API Instance.")
        API = tweepy.API(auth)

    def tweet(self, txt):
        print("'{}'をツイートします".format(txt))
        print("ツイートしています...")
        sleep(1)
        API.update_status(txt)
        print("ツイート完了しました")

    def get_mytimeline(self, count):
        print("最新の投稿から{}件を取得します".format(count))
        print("取得中...")
        sleep(2)
        results = API.home_timeline(count=count)
        for num, text in enumerate(results):
            print(str(num+1)+"件目: ", text.text)

    def get_usertimeline(self, id, count):
        #result = []
        try:
            #status = API.user_timeline(id, page=page_num, tweet_mode="extended")
            status = tweepy.Cursor(API.user_timeline, id=id, tweet_mode="extended").pages(count)
            print("'{}'のユーザー情報を取得しました".format(id))
        except Exception as e:
                print(e)
        return status


    def search_word(self, word, count):
        print("{}でキーワード検索します".format(word))
        print("検索中...")
        sleep(2)
        results = API.search(q=word, lang="ja", count=count)
        for num, result in enumerate(results):
            try:
                display = result.text.encode("utf-8", "ignore").decode("utf-8")
                print(display, "\n", (num+1), "件目の投稿")
                print("-"*100)
            except:
                pass
