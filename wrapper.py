import pydaisi as pyd
import pandas as pd
import streamlit as st

tw_daisi = pyd.Daisi("erichare/Twitter Search")
sa_daisi = pyd.Daisi("erichare/Sentiment Analysis")

def get_twitter_sentiment(query: str, count: int=100, tweets=None):
    '''
    Interface with the Twitter API to fetch tweets related to the given query and derive the sentiment
    
    This function wraps two other Daisies in order to derive the sentiment of tweets related
    to the given query

    :param str query: The search query to provide to Twitter
    :param int count: The maximum number of tweets to retrieve
    
    :return: Author and text of tweets related to the given query, along with the sentiment of each
    '''

    if tweets is None:
        tweets = tw_daisi.fetch_tweets(query, count).value

    sentiment = sa_daisi.get_sentiment([x for x in tweets["text"].tolist()]).value

    tweets["label"] = [x["label"] for x in sentiment]
    tweets["score"] = [x["score"] for x in sentiment]

    return tweets

if __name__ == "__main__":
    st.set_page_config(layout = "wide")
    st.title("Twitter Sentiment Analysis with Daisies")

    st.markdown("This Wrapper Daisi calls two other Daisies, the [Twitter Search](https://app.daisi.io/daisies/5636b873-4ed9-44c2-a737-ad9b95dedfba/info) Daisi, and the [Sentiment Analysis](https://dev3.daisi.io/daisies/dd7ca16b-efeb-47b4-80ca-2f77ef106739/info) Daisi, to perform a Sentiment Analysis of the ten most recent tweets related to your query!")
    st.markdown("NOTE: Please use PyDaisi and the API interface for processing more than 100 tweets!")

    with st.sidebar:
        query = st.text_input('Twitter Search Keyword', 'Daisi Python')
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

    tweets = tw_daisi.fetch_tweets(query, count).value

    final_results = []
    element = st.empty()
    with st.spinner('Fetching tweets and computing sentiment...'):
        for i in range(0, count, 10):
            max_ind = min(tweets.shape[0], i + 10)

            my_sent = get_twitter_sentiment(query, count=count, tweets=tweets[i:max_ind])
            final_results.append(my_sent)
            element.empty()
            element = st.dataframe(pd.concat(final_results))

    st.success('Done!')
