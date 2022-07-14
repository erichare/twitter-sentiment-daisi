# Twitter Sentiment Analysis with Daisies

## How to Call

First, we simply load the PyDaisi package:

```python
import pydaisi as pyd
```

Next, we connect to the Daisi:

```python
twitter_sentiment = pyd.Daisi("erichare/Twitter Sentiment")
```

Next, let's provide a query to search Twitter with:

```python
twitter_sentiment.get_twitter_sentiment(query="Daisi", count=10).value
```

And that's it! We have a clean dataframe containing the author of the tweet and the text of the tweet based on the query, and the sentiment of each of the tweets!
