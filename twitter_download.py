import pandas as pd
import tweepy
import os

import tweepy
bearer_token = 'INSERT TOKEN HERE'
client = tweepy.Client(bearer_token=bearer_token)


def get_tweets(query, limit=100):
  '''
  query: the search query for twitter (Requried)
  limit: maximum number of tweets to retrieve, default = 100 tweets

  returns a dataframe object of tweets retrieved by the search query

  check this article to understand the format of queries 
  https://medium.com/@robguilarr/making-queries-to-twitter-api-on-tweepy-66afeb7184a4
  '''

  tweets = client.search_recent_tweets(query=query, max_results=limit)

  # Create columns for the DataFrame
  columns = ['tweet']
  tweets_data = []

##check if twitter api returned 0 results
  try:
      len(tweets[0])
  except TypeError:
      return pd.DataFrame(["no results"], columns=columns)

  for i in range(len(tweets[0])):
    #print(str(tweets[0][i]))

    tweets_data.append(str(tweets[0][i]))

  # Create a dataframe with the results
  return pd.DataFrame(tweets_data, columns=columns)

def get_examples(terms, query_extra="", limit=100):
  examples_dict = {}
  for term in terms:
    ###you can edit the query here by changing the paramater "query_extra"
    print("getting tweets for {}".format(term))
    examples_dict[term] = get_tweets("{} {}".format(term, query_extra), limit=limit)

  return examples_dict

def convert_dict_to_csv(df_dict, lang):
  if not os.path.exists('Twitter Examples/'):
   os.makedirs('Twitter Examples/')
  if not os.path.exists('Twitter Examples/{}/'.format(lang)):
   os.makedirs('Twitter Examples/{}/'.format(lang))
  for key, df in df_dict.items():
    df.to_csv('Twitter Examples/{}/{}.csv'.format(lang, key))


if __name__ == "__main__":
    SHEET_ID = '1cTDvhpsvd0YwQGj0IfgY_tkS1wKsazo0kh5DRx4e_7k'
    SHEET_NAME = 'Sheet1'
    sheet_link = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(sheet_link, on_bad_lines='skip')
    df["L"] = df["L"].fillna(method='ffill').apply(lambda x: x.capitalize())
    terms = df["Term"].apply(lambda x: x.split('\n')[0])
    languages = ["English", "Russian", "Spanish", "Urdu", "Arabic"]
    for lang in languages:
        print("getting examples for {}".format(lang))
        terms_lang = df[df["L"] == lang]["Term"].apply(lambda x: x.split('\n')[0])
        examples_dict = get_examples(terms_lang, query_extra="", limit=100)
        convert_dict_to_csv(examples_dict, lang)


