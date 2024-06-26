# -*- coding: utf-8 -*-
"""mth208-mbb-state-webscraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GlRHfwf4VK0qGejvnPxJ8yvhUZn_fsMA
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load your existing dataset
df = pd.read_csv('cbb23.csv')
teams = df.iloc[:,0]

# remove periods
teams = teams.replace(to_replace='\.', value='', regex=True)


# Scrape the data from the webpage
url = 'https://www.ncsasports.org/mens-basketball/division-1-colleges'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)

print(response.status_code)  # Should be 200 for a successful request
print(response.text[:500])  # Print the first 500 characters of the response text

soup = BeautifulSoup(response.content, 'html.parser')

# Extract team names and locations from the webpage
team_locations = {}
for row in soup.select('.college-list .row'):
    # print(row)  # To see what each row contains
    # Find the team name
    team_name_element = row.find('div', itemprop='name')
    if team_name_element:
        # print(team_name_element)  # To check if team names are being found
        team_name = team_name_element.get_text(strip=True)

        # Find the state
        state_element = row.find('span', itemprop='addressRegion')
        if state_element:
            # print(state_element)  # To check if states are being found
            state = state_element.get_text(strip=True)
            team_locations[team_name] = state

# Function to match team names from your dataset with scraped data
def get_location(team, team_locations):
    # Iterate through the keys (team names) in the dictionary
    for team_name in team_locations.keys():
        # Check if the provided team is part of the website's team name
        if team.lower() in team_name.lower():
            # Return the corresponding location
            return team_locations[team_name]

    # Return 'Not Found' if no match is found
    return 'Not Found'

# Update your dataset with the locations
df['Location'] = teams.apply(lambda x: get_location(x, team_locations))

# Save the updated dataset
df.to_csv('updated_cbb23.csv', index=False)