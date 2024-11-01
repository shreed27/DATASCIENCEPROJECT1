# -*- coding: utf-8 -*-
"""IITROORKEEINTERNcovid_19_tweets.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zHKtXAiGLQB1xv9lCdDX9VXWkeAUTSrN

#***DATA SCIENCE PROJECT***
### - IIT Roorkee Data Science Project Intern
#### - A data science notebook using tweets to make conclusions regarding the COVID-19 virus. Analyse tweets to see trends in certain areas.


### **DATA:**
###1. Public tweets that include #covid19
#####       https://www.kaggle.com/gpreda/covid19-tweets
###       2. ISO country codes (for the last part of the project)
#####       https://www.kaggle.com/andradaolteanu/iso-country-codes-global
"""

# Commented out IPython magic to ensure Python compatibility.
# imports
import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
from wordcloud import WordCloud, STOPWORDS

from google.colab import drive
drive.mount('/content/gdrive')
# %cd /content/gdrive/My\ Drive/data/tweets

# load data
tweets_df = pd.read_csv("covid19_tweets.csv")

# get shape of the data
print(f"data shape: {tweets_df.shape}")

# get features of the data
tweets_df.info()

# data description
tweets_df.describe()

# what does untouched data look like
tweets_df.head()

# missing data
def missing_data(data):
    total = data.isnull().sum()
    percent = (data.isnull().sum()/data.isnull().count()*100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return(np.transpose(tt))

# show missing data
missing_data(tweets_df)

# unique values
def unique_values(data):
    total = data.count()
    tt = pd.DataFrame(total)
    tt.columns = ['Total']
    uniques = []
    for col in data.columns:
        unique = data[col].nunique()
        uniques.append(unique)
    tt['Uniques'] = uniques
    return(np.transpose(tt))

# show unique values
unique_values(tweets_df)

# find most frequent values
def most_frequent_values(data):
    total = data.count()
    tt = pd.DataFrame(total)
    tt.columns = ['Total']
    items = []
    vals = []
    for col in data.columns:
        itm = data[col].value_counts().index[0]
        val = data[col].value_counts().values[0]
        items.append(itm)
        vals.append(val)
    tt['Most frequent item'] = items
    tt['Frequence'] = vals
    tt['Percent from total'] = np.round(vals / total * 100, 3)
    return(np.transpose(tt))

# show frequent values
most_frequent_values(tweets_df)

# VISUALIZATION METHOD
def plot_count(feature, title, df, size=1):
    f, ax = plt.subplots(1,1, figsize=(4*size,4))
    total = float(len(df))
    g = sns.countplot(df[feature], order = df[feature].value_counts().index[:20], palette='Set3')
    g.set_title("Number and percentage of {}".format(title))
    if(size > 2):
        plt.xticks(rotation=90, size=8)
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                height + 3,
                '{:1.2f}%'.format(100*height/total),
                ha="center")
    plt.show()

# usernames related to trending covid-19 topics
plot_count("user_name", "User name", tweets_df,4)

# user location in high-risk areas
plot_count("user_location", "User location", tweets_df,4)

# What are the sources of these tweets?
plot_count("source", "Source", tweets_df,4)

# WORDCLOUD SETUP
stopwords = set(STOPWORDS)

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=50,
        max_font_size=40,
        scale=5,
        random_state=1
    ).generate(str(data))

    fig = plt.figure(1, figsize=(10,10))
    plt.axis('off')
    if title:
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

# PREVALENT WORDS IN ALL OF TWITTER
show_wordcloud(tweets_df['text'], title = 'Prevalent words in tweets')

# PREVALENT WORDS ACROSS THE US
us_df = tweets_df.loc[tweets_df.user_location=="United States"]
show_wordcloud(us_df['text'], title = 'Prevalent words in tweets from US')

# PREVALENT WORDS ACROSS THE UK
us_df = tweets_df.loc[tweets_df.user_location=="United Kingdom"]
show_wordcloud(us_df['text'], title = 'Prevalent words in tweets from UK')

# PREVALENT WORDS ACROSS CANADA
us_df = tweets_df.loc[tweets_df.user_location=="Canada"]
show_wordcloud(us_df['text'], title = 'Prevalent words in tweets from Canada')

# HASHTAG ANALYSIS
def plot_features_distribution(features, title, df, isLog=False):
    plt.figure(figsize=(12,6))
    plt.title(title)
    for feature in features:
        if(isLog):
            sns.distplot(np.log1p(df[feature]),kde=True,hist=False, bins=120, label=feature)
        else:
            sns.distplot(df[feature],kde=True,hist=False, bins=120, label=feature)
    plt.xlabel('')
    plt.legend()
    plt.show()

tweets_df['hashtags'] = tweets_df['hashtags'].replace(np.nan, "['None']", regex=True)
tweets_df['hashtags'] = tweets_df['hashtags'].apply(lambda x: x.replace('\\N',''))
tweets_df['hashtags_count'] = tweets_df['hashtags'].apply(lambda x: len(x.split(',')))
plot_features_distribution(['hashtags_count'], 'Hashtags per tweet (all data)', tweets_df)

tweets_df['hashtags_individual'] = tweets_df['hashtags'].apply(lambda x: x.split(','))
from itertools import chain
all_hashtags = set(chain.from_iterable(list(tweets_df['hashtags_individual'])))
print(f"There are totally: {len(all_hashtags)}")

# COUNTRY ANALYSIS
country_df = pd.read_csv("wikipedia-iso-country-codes.csv")

# what does this data look like
country_df.columns = ["country", "alpha2", "alpha3", "numeric", "iso"]
country_df.head()

# merge the countries dataset with the tweets dataset
tweets_df['country'] = tweets_df['user_location']
tweets_df = tweets_df.merge(country_df, on="country")

# what does this data look like
tweets_df.head(5)

# use plotly to visualize data across the world

tw_add_df = tweets_df.groupby(["country", "iso", "alpha3"])['text'].count().reset_index()
tw_add_df.columns = ["country", "iso", "alpha3", "tweets"]

import plotly.express as px

def plot_map(dd_df, title):
    hover_text = []
    for index, row in dd_df.iterrows():
        hover_text.append((f"country: {row['country']}<br>tweets: {row['tweets']}\
                          <br>country code: {row['iso']}<br>country alpha3: {row['alpha3']}"))
    dd_df['hover_text'] = hover_text

    fig = px.choropleth(dd_df,
                        locations="alpha3",
                        hover_name='hover_text',
                        color="tweets",
                        projection="natural earth",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        width=900, height=700)
    fig.update_geos(
        showcoastlines=True, coastlinecolor="DarkBlue",
        showland=True, landcolor="LightGrey",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="Blue",
        showrivers=True, rivercolor="Blue",
        showcountries=True, countrycolor="DarkBlue"
    )
    fig.update_layout(title = title, geo_scope="world")
    fig.show()

# plot result
plot_map(tw_add_df, "Tweets per country (where country is specified)")