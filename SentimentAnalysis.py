import praw
import pandas as pd
import datetime
import numpy as np
import spacy
import plotly.express as px
from spacy import displacy
from collections import Counter

'''
The r/stocks subreddit is a discussion forum relating to investing.
This program finds the most frequently mentioned company names in the r/stocks subreddit
Posts can be searched by "new" (newest posts in the subreddit), 
                         "top" (most popular posts in the subreddit),
                         "hot" (trending posts in the subreddit)
The data is parsed using a natural language processing library (spacy) and generates a bar graph
Different subreddits such as r/investing can be put in the place of r/stocks
This data can be used to see what companies people are talking about in the investing world
Future projects can include peoples positive/negative views on these companies
'''

# expand panda width in console
desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',10)

# link reddit API credentials
# THE CODE WILL NOT WORK WITHOUT DOING SO
# unfortunately I am not allowed to provide you with my credentials - but signing up for API access is very easy
# more info can be found here: https://www.reddit.com/wiki/api#wiki_read_the_full_api_terms_and_sign_up_for_usage
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')

# choose how many results to show in the resulting bar graph
num_of_results = 20

# choose subreddit to pull data from: default = https://www.reddit.com/r/stocks/
submissions = reddit.subreddit('stocks').top(limit=None)

# create dataframe containing the title, score (upvotes), id, and URL
df = pd.DataFrame([[x.title, x.score, x.id, x.url] for x in submissions], columns=['title', 'score', 'id', 'url'])

# upacy is our natural language processing library
# using spacy we identify company names in the subreddit post titles
# spacy is not perfect, and unfortunately neglects to identify certain company names
nlp = spacy.load("en_core_web_sm")

# use spacy to parse through the dataframe and find company names identified by the label "ORG"
def spacy_parse(df, label='ORG'):
    titles = df['title']
    array = []
    for title in titles:
        names = []
        title = title.replace("'s", "")  # clean titles
        doc = nlp(title)
        for title_label in doc.ents:
            if title_label.label_ == label:
                names.append(title_label.text)
        array.append(names)
    return array

# adds column in dataframe containing company name(s) in the post title
df['data']= spacy_parse(df)

# displays dataframe (optional - you can comment out this part and it wont effect the graph)
print(df)

# simple function that creates a graph of our data
def plot(df):
    graph = px.bar(df, x='Number of Times Mentioned', y='Company Name', orientation='h')
    return graph

# create list of company names mentioned in the subreddit (contains duplicates)
list_of_company_names = [i for names in df['data'] for i in names]

# creates dictionary with each company name followed by the number of times it appears in the subreddit
name_count_dictionary = Counter(list_of_company_names)

# create a simple dataframe with each company name followed by the number of times it appears in the subreddit
results = pd.DataFrame(name_count_dictionary.most_common(num_of_results), columns=['Company Name', 'Number of Times Mentioned'])

# finally, plot the chart (you can use Jupyter to view result)
plot(results)
