import pydaisi as pyd
import pandas as pd
import streamlit as st

tw_daisi = pyd.Daisi("erichare/Twitter Search", instance="dev3")
sa_daisi = pyd.Daisi("erichare/Sentiment Analysis", instance="dev3")

def get_twitter_sentiment(query: str, count: int=10):
    '''
    Interface with the Twitter API to fetch tweets related to the given query and derive the sentiment
    
    This function wraps two other Daisies in order to derive the sentiment of tweets related
    to the given query

    :param str query: The search query to provide to Twitter
    :param int count: The maximum number of tweets to retrieve
    
    :return: Author and text of tweets related to the given query, along with the sentiment of each
    '''

    result = tw_daisi.fetch_tweets(query, count).value
    sentiment = sa_daisi.get_sentiment([x for x in result["text"].tolist()]).value

    result["label"] = [x["label"] for x in sentiment]
    result["score"] = [x["score"] for x in sentiment]

    return result

if __name__ == "__main__":
    st.set_page_config(layout = "wide")
    st.title("Twitter Sentiment Analysis with Daisies")

    st.markdown("This Wrapper Daisi calls two other Daisies, the [Twitter Search](https://dev3.daisi.io/daisies/4602e8b6-127b-4d1f-b13c-60d7b7b7431b/info) Daisi, and the [Sentiment Analysis](https://dev3.daisi.io/daisies/dd7ca16b-efeb-47b4-80ca-2f77ef106739/info) Daisi, to perform a Sentiment Analysis of the ten most recent tweets related to your query!")

    with st.sidebar:
        query = st.text_input('Twitter Search Keyword', 'Daisi Python')

    with st.expander("Inference with PyDaisi", expanded=True):
        st.markdown(f"""
        ```python
        import pydaisi as pyd

        twitter_sentiment = pyd.Daisi("erichare/Twitter Sentiment", instance="dev3")
        result = twitter_sentiment.get_twitter_sentiment("{query}").value
        
        result
        ```
        """)

    st.table(data=get_twitter_sentiment(query))