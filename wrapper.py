import pydaisi as pyd

tw_daisi = pyd.Daisi("erichare/Twitter Search", instance="dev3")
sa_daisi = pyd.Daisi("erichare/Sentiment Analysis", instance="dev3")

def get_twitter_sentiment(query: str, count: int=10):
    result = tw_daisi.fetch_tweets(query, count).value
    sentiment = sa_daisi.get_sentiment([x for x in result["text"].tolist()]).value

    result["label"] = [x["label"] for x in sentiment]
    result["score"] = [x["score"] for x in sentiment]

    return result
