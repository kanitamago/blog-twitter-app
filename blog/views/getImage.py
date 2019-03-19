from blog.views.script import twitter
from flask import Flask, render_template, request, redirect, url_for
import time
import random
import tweepy
from blog import app

api = twitter.Create_api()

@app.route("/works/getimages")
def display_getimage():
    q = random.sample(range(1, 9999), 1)[0]
    return render_template("works/getImage.html", q=q)

@app.route("/works/gettweets")
def display_gettweet():
    q = random.sample(range(1, 9999), 1)[0]
    return render_template("works/getTweet.html", q=q)

@app.route("/works/getimages", methods=["GET", "POST"])
def getImage():
    q = random.sample(range(1, 9999), 1)[0]
    if request.method == "POST":
        id = request.form["id"]
        count = request.form["count"]
        if id == "" or count == "":
            return render_template("works/getImage.html", error="漏れなく入力してください", q=q)
        try:
            count = int(count)
        except:
            return render_template("works/getImage.html", error="取得ページ数には整数を入力してください", q=q)
        results = api.get_usertimeline(id=id, count=count)
        get_tweets = 0
        get_photos = 0
        urls = []
        texts = []
        times = []
        tweetset = []
        try:
            for idx, page in enumerate(results):
                print("{}ページ目のツイート解析".format(idx+1))
                for tweet in page:
                    get_tweets += 1
                    try:
                        for media in tweet.extended_entities["media"]:
                            urls.append(media["media_url"])
                            texts.append(tweet._json["full_text"])
                            times.append(tweet.created_at)
                            get_photos += 1
                    except:
                        pass
                    #print("Imageがありません")
        except:
            return render_template("works/getImage.html", error="ユーザーが存在しない、もしくはロックされています", q=q)
        texts = texts[::-1]
        urls = urls[::-1]
        times = times[::-1]
        for sets in zip(urls, texts, times):
            tweetset.append(sets)
        return render_template("works/getImage.html", results=tweetset, display_gb="display_gb",
                                get_counts="計"+str(get_tweets)+"件中"+str(get_photos)+"枚の画像を取得しました", q=q)

@app.route("/works/gettweets", methods=["GET", "POST"])
def getTweet():
    q = random.sample(range(1, 9999), 1)[0]
    get_tweets = 0
    if request.method == "POST":
        id = request.form["id"]
        count = request.form["count"]
        if id == "" or count == "":
            return render_template("works/getTweet.html", error="漏れなく入力してください", q=q)
        try:
            count = int(count)
        except:
            return render_template("works/getTweet.html", error="取得ページ数には整数を入力してください", q=q)
        status = api.get_usertimeline(id=id, count=count)
        tweets = []
        times = []
        user_tweets = []
        prof_img = set()
        try:
            for page in status:
                for tweet in page:
                    prof_img.add(tweet._json["user"]["profile_image_url"])
                    get_tweets += 1
                    tweets.append(tweet._json["full_text"])
                    times.append(tweet.created_at)
        except:
            return render_template("works/getTweet.html", error="ユーザーが存在しない、もしくはロックされています", q=q)
        tweets = tweets[::-1]
        times = times[::-1]
        for sets in zip(tweets, times):
            user_tweets.append(sets)
        return render_template("works/getTweet.html", id="@"+str(id)+"さんのツイート", user_tweets=user_tweets, get_tweets=str(get_tweets)+"ツイート取得しました", prof_img="src="+list(prof_img)[0], q=q)
