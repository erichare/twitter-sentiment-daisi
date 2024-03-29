import pydaisi as pyd
import pandas as pd
import streamlit as st # For UI support

def _tweet_fetch(query, count):
    tw_daisi = pyd.Daisi("erichare/Twitter Search")
    tweets = tw_daisi.fetch_tweets(query, count).value

    return tweets

def get_twitter_sentiment(query: str, count: int=10, tweets=None):
    '''
    Interface with the Twitter API to fetch tweets related to the given query and derive the sentiment
    
    This function wraps two other Daisies in order to derive the sentiment of tweets related
    to the given query

    :param str query: The search query to provide to Twitter
    :param int count: The maximum number of tweets to retrieve
    
    :return: Author and text of tweets related to the given query, along with the sentiment of each
    '''

    if tweets is None:
        tw_daisi = pyd.Daisi("erichare/Twitter Search")
        tweets = tw_daisi.fetch_tweets(query, count).value

    sa_daisi = pyd.Daisi("erichare/Sentiment Analysis")
    sentiment = sa_daisi.get_sentiment([x for x in tweets["text"].tolist()]).value

    tweets["sentiment"] = [x["label"] for x in sentiment]
    tweets["score"] = [x["score"] for x in sentiment]

    return tweets

if __name__ == "__main__":
    st.set_page_config(layout = "wide")
    st.title("Twitter Sentiment Analysis with Daisies")

    st.markdown("## Information")

    st.markdown("This Wrapper Daisi calls two other Daisies, the [Twitter Search](https://app.daisi.io/daisies/erichare/Twitter%20Search/info) Daisi, and the [Sentiment Analysis](https://app.daisi.io/daisies/erichare/Sentiment%20Analysis/info) Daisi, to perform a Sentiment Analysis of the N most recent tweets related to your query!")
    st.markdown("NOTE: Please use PyDaisi and the API interface for processing more than 100 tweets!")

    with st.sidebar:
        query = st.text_input('Twitter Search Keyword', 'Python')
        count = st.number_input("Number of Tweets", min_value=1, max_value=100, value=10, step=1)

    with st.expander("Inference with PyDaisi", expanded=True):
        st.markdown(f"""
        ```python
        import pydaisi as pyd

        twitter_sentiment = pyd.Daisi("erichare/Twitter Sentiment")
        result = twitter_sentiment.get_twitter_sentiment("{query}", count={count}).value
        
        result
        ```
        """)

    st.markdown("## Tweet Sentiment")
    tweets = _tweet_fetch(query, count)

    final_results = []
    element = st.empty()
    with st.spinner('Fetching tweets and computing sentiment...'):
        for i in range(0, count, 10):
            max_ind = min(tweets.shape[0], i + 10)

            my_sent = get_twitter_sentiment(query, count=count, tweets=tweets[i:max_ind])
            final_results.append(my_sent)

            element.empty()
            element = st.table(pd.concat(final_results))

    st.markdown("## Aggregate Results")

    res = pd.concat(final_results).groupby(['sentiment']).size().to_frame(name = 'size').reset_index()
    res.columns = ["Sentiment", "Number of Tweets"]

    st.table(res)
