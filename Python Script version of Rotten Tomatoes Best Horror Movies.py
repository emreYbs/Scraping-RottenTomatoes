#EmreYbs

# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Set-up

# %%
# load packages
import requests
from bs4 import BeautifulSoup


# %%
# Give the URL of the site. For Pandas DF and csv output, some url's can give better results
base_site = "https://editorial.rottentomatoes.com/guide/best-horror-movies-of-all-time/"


# %%
# sending a request to the webpage
response = requests.get(base_site)
response.status_code


# %%
# get the HTML from the webpage
html = response.content

# %% [markdown]
# ## Choosing a parser
# %% [markdown]
# ### html.parser

# %%
# convert the HTML to a Beautiful Soup object
soup = BeautifulSoup(html, 'html.parser')


# %%
# Exporting the HTML to a file
with open('Rotten_tomatoes_page_2_HTML_Parser.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))

# %% [markdown]
# ### lxml

# %%
# convert the HTML to a BeatifulSoup object
soup = BeautifulSoup(html, 'lxml')


# %%
# Exporting the HTML to a file
with open('Rotten_tomatoes_page_2_LXML_Parser.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))

# %% [markdown]
# ### A word of caution
# %% [markdown]
# ## Finding an element containing all the data

# %%
# Finding all div tags on the webpage containing the information we want to scrape
divs = soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
divs

# %% [markdown]
# # Extracting the title, year and score of each movie

# %%

divs[0].find("h2")


# %%
# Extracting all 'h2' tags
headings = [div.find("h2") for div in divs]
headings


# %%
# Inspecting the text inside the headings
[heading.text for heading in headings]


# %%
# It does contain the info we want to extract
# However, we need to obtain the title, year and score separately
# Let's inspect one heading to see if there is a way to distinguish between them
headings[0]


# %%
# We notice that:

# The movie title is in the 'a' tag
# The year is in a 'span' with class 'start-year'
# The score is in a 'span' with class 'tMeterScore'

# %% [markdown]
# ## Title

# %%
# Let's check all heading links
[heading.find('a') for heading in headings]


# %%
# Obtaining the movie titles from the links
movie_names = [heading.find('a').string for heading in headings]
movie_names

# %% [markdown]
# ## Year

# %%
# Filtering only the spans containing the year
[heading.find("span", class_ = 'start-year') for heading in headings]


# %%
# Extracting the year string
years = [heading.find("span", class_ = 'start-year').string for heading in headings]
years


# %%
years[0]

# %% [markdown]
# ### Removing the brackets

# %%
# One way to remove the brackets is to drop the first and last symbol of the string
years[0][1:-1]


# %%
# However, this will break, if the format of the year is changed


# %%
# Alternativelly, we can do it with the help of the strip() method (this is robust)

# It removes leading and trailing symbols from a string
# By default, it removes whitespace, but we can specify other symbols to strip


# %%
# Removing '('
years[0].strip('(')


# %%
# Removing ')'
years[0].strip(')')


# %%
# Combining both
years[0].strip('()')


# %%
# Updating years with stripped values
years = [year.strip('()') for year in years]
years


# %%
# Converting all the strings to integers
years = [int(year) for year in years]
years

# %% [markdown]
# ## Score

# %%

# Filtering only the spans containing the score
[heading.find("span", class_ = 'tMeterScore') for heading in headings]


# %%
# Extracting the score string
scores = [heading.find("span", class_ = 'tMeterScore').string for heading in headings]
scores


# %%
# Removing the '%' sign
scores = [s.strip('%') for s in scores]
scores


# %%
# Converting each score to an integer
scores = [int(s) for s in scores]
scores

# %% [markdown]
# # Extracting the rest of the information
# %% [markdown]
# ## Critics Consensus

# %%
# Getting the 'div' tags containing the critics consensus
consensus = [div.find("div", {"class": "info critics-consensus"}) for div in divs]
consensus


# %%
# Inspecting the text inside these tags
[con.text for con in consensus]

# %% [markdown]
# ### Way #1: Text processing

# %%

common_phrase = 'Critics Consensus: '


# %%

len(common_phrase)


# %%
consensus[0].text


# %%

consensus[0].text[19:]


# %%

common_len = len(common_phrase)


# %%
# Cleaning the list of the common phrase
consensus_text = [con.text[common_len:] for con in consensus]
consensus_text


# %%
# We can add if-else logic to only truncate the string in case it starts with the common phrase
consensus_text = [con.text[common_len:] if con.text.startswith(common_phrase) else con.text for con in consensus ]
consensus_text

# %% [markdown]
# ### Way #2: Inspecting the HTML

# %%
consensus[0]


# %%
# When inspecting the HTML we see that the common phrase ("Critics Consensus: ")
# is located inside a span element
# The string we want to obtain follows that


# %%
# We can use .contents to obtain a list of all children of the tag
consensus[0].contents


# %%
# The second element of that list is the text we want
consensus[0].contents[1]


# %%
# We can remove the extra whitespace (space at the beginning) with the .strip() method
consensus[0].contents[1].strip()


# %%
# Processing all texts
consensus_text = [con.contents[1].strip() for con in consensus]
consensus_text


# %%
# In my opinion, this method is closer to the BeautifulSoup approach

# %% [markdown]
# ## Directors

# %%
# Extracting all director divs
directors = [div.find("div", class_ = 'director') for div in divs]
directors


# %%
# Inspecting a div
directors[0]


# %%
# The director's name can be found as the string of a link

# Obtaining all director links
[director.find("a") for director in directors]


# %%
# Notice that one link is None - the director of Iron Man is missing!

# This means we can't simply use .string,
# because None has no string attribute


# %%
# Running the line below will raise an error if uncommented

#[director.find("a").string for director in directors]


# %%
# We can use if-else to deal with the None value

final_directors = [None if director.find("a") is None else director.find("a").string for director in directors]
final_directors

# %% [markdown]
# ## Cast info

# %%
cast_info = [div.find("div", class_ = 'cast') for div in divs]
cast_info


# %%
cast_info[0]


# %%
# Each cast member's name is the string of a link
# There are multiple cast members for a movie


# %%
# Let's first practice with a single movie

# Obtain all the links to different cast members
cast_links = cast_info[0].find_all('a')
cast_links


# %%
# Extract the names from the links
cast_names = [link.string for link in cast_links]
cast_names


# %%
# OPTIONALLY: We can stitch all names together as one string

# This can be done using the join method
# To use join, pick a string to use as a separator (in our case a comma, followed with a space) and
# pass the list of strings you want to merge to the join method

cast = ", ".join(cast_names)
cast


# %%
# Now we need to do the above operations for every movie

# We can either use a for loop (clearer), or
# use a nested list compehension (more concise)

# %% [markdown]
# ### Using a for loop

# %%
# Initialize the list of all cast memners
cast = []

# Just put all previous operations inside a for loop
for c in cast_info:
    cast_links = c.find_all('a')
    cast_names = [link.string for link in cast_links]
    
    cast.append(", ".join(cast_names)) # Joining is optional

cast

# %% [markdown]
# ### Nested list comprehension

# %%
# As you can see this can be done in just one line using nested list comprehension
# However, the code is harded to understand

cast = [", ".join([link.string for link in c.find_all("a")]) for c in cast_info]
cast

# %% [markdown]
# ## Adjusted score

# %%


# The adjusted scores can be found in a div with class 'info countdown-adjusted-score'
adj_scores = [div.find("div", {"class": "info countdown-adjusted-score"}) for div in divs]
adj_scores


# %%
# Inspecting an element
adj_scores[0]


# %%
# By inspection we see that the string we are looking for is the second child of the 'div' tag
adj_scores[0].contents[1]  # Note the extra whitespace at the end


# %%
# Extracting the string (without '%' sign and extra space)
adj_scores_clean = [score.contents[1].strip('% ') for score in adj_scores]
adj_scores_clean


# %%
# Converting the strings to numbers
final_adj = [float(score) for score in adj_scores_clean] # Note that this time the scores are float, not int!
final_adj

# %% [markdown]
# ## Synopsis

# %%


# The synopsis is located inside a 'div' tag with the class 'info synopsis'
synopsis = [div.find('div', class_='synopsis') for div in divs]
synopsis


# %%
# Inspecting the element
synopsis[0]


# %%
# The text is the second child
synopsis[0].contents[1]


# %%
# Extracting the text
synopsis_text = [syn.contents[1] for syn in synopsis]
synopsis_text

# %% [markdown]
# # Representing the data in structured form

# %%

import pandas as pd

# %% [markdown]
# ## Creating a Data Frame

# %%
# A dataframe is a tabular data type, frequently used in data science

movies_info = pd.DataFrame()
movies_info  # The dataframe is still empty, we need to fill it with the info we gathered

# %% [markdown]
# ## Populating the dataframe

# %%
# Populating the dataframe

movies_info["Movie Title"] = movie_names
movies_info["Year"] = years
movies_info["Score"] = scores
movies_info["Adjusted Score"] = final_adj  # Homework
movies_info["Director"] = final_directors
movies_info["Synopsis"] = synopsis_text    # Homework
movies_info["Cast"] = cast
movies_info["Consensus"] = consensus_text

# Let's see how it looks
movies_info


# %%
# By default pandas abbreviates any text beyond a certain length (as seen in the Cast and Consensus columns)

# We can change that by setting the maximum column width to -1,
# which means the column would be as wide as to display the whole text
pd.set_option('display.max_colwidth', -1)
movies_info

# %% [markdown]
# ## Exporting the data to CSV (comma-separated values) and excel files

# %%
# Write data to excel file
movies_info.to_excel("movies_info.xlsx", index = False, header = True)


# %%
# or write data to CSV file
movies_info.to_csv("movies_info.csv", index = False, header = True)


# %%
# Index is set to False so that the index (0,1,2...) of each movie is not saved to the file (the index is purely internal)
# The header is set to True, so that the names of the columns are saved


