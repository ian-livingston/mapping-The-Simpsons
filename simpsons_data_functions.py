import pandas as pd
import numpy as np
import time
import requests
import re
from bs4 import BeautifulSoup
from datetime import date
from fake_useragent import UserAgent

# For getting episode vitals from IMDB
def get_simpsons_data(seasons):
    '''
    Arguments: A list of season numbers (ints)
    Returns: A dict of data for every season
  
    Notes: Length of URL varies around season 30
    '''

    ua = UserAgent()
    user_agent = {'User-agent': ua.random}
    all_simpsons_data = {}
    
    for season in seasons:
        url = "https://www.imdb.com/title/tt0096697/episodes?season={}".format(str(season))
        response = requests.get(url, headers=user_agent)
        print("Season {} request status code: {}".format(str(season), str(response.status_code)))
        page = response.text
        simp_soup = BeautifulSoup(page)
        
        season_eps = simp_soup.find("div", class_="list detail eplist").find_all("div", class_=re.compile("^(list_item )(odd|even)$"))
        season_dict = {}
        
        for i, episode in enumerate(season_eps):
            ep_details = episode.find("div", class_="info")
            ep_name = ep_details.find("a", itemprop="name").text

            inner_dict = {}
            ep_number = int(ep_details.find("meta")["content"])
            ep_airdate = pd.to_datetime(ep_details.find("div", class_="airdate").text.strip())
            ep_rating = float(ep_details.find("span", class_="ipl-rating-star__rating").text)
            ep_rating_count = int(ep_details.find("span", class_="ipl-rating-star__total-votes").text.strip('()').replace(",", ""))
            ep_description = ep_details.find("div", class_="item_description").text.strip()
            inner_dict["Season"] = season
            inner_dict["Episode number"] = ep_number
            inner_dict["Airdate"] = ep_airdate
            inner_dict["Description"] = ep_description
            inner_dict["Rating"] = ep_rating
            inner_dict["Number of ratings"] = ep_rating_count
            
            # Heading to the episode's "Full Cast & Crew" page for more data
            if season <= 30 and ep_number <= 20:    
                url_part = episode.find("a", itemprop="name")["href"]
                ep_url = "https://www.imdb.com{}{}".format(url_part[:17], "fullcredits")
                ep_response = requests.get(ep_url, headers=user_agent)
                print("Season {} Episode {} request status code: {}".format(str(season), str(i+1), str(ep_response.status_code)))
                ep_page = ep_response.text
                ep_soup = BeautifulSoup(ep_page)

                director_and_writers = ep_soup.find_all("table", class_="simpleTable simpleCreditsTable")
                ep_director = director_and_writers[0].find("td", class_="name").findNext().text.strip()
                ep_writers = []
                for person in director_and_writers[1].find_all("td", class_="name"):
                    ep_writers.append(person.findNext().text.strip() + " " + person.findNext("td", class_="credit").text.strip())
                characters = []
                for group in ep_soup.find_all("td", class_="character"):
                    for _ in group.find_all("a"):
                        characters.append(_.text)           
                inner_dict["Director"] = ep_director
                inner_dict["Writers"] = ep_writers
                inner_dict["Characters"] = characters
                time.sleep(3.7)

                season_dict[ep_name] = inner_dict
            
            else:
                url_part = episode.find("a", itemprop="name")["href"]
                ep_url = "https://www.imdb.com{}{}".format(url_part[:18], "fullcredits")
                ep_response = requests.get(ep_url, headers=user_agent)
                print("Season {} Episode {} request status code: {}".format(str(season), str(i+1), str(ep_response.status_code)))
                ep_page = ep_response.text
                ep_soup = BeautifulSoup(ep_page)

                director_and_writers = ep_soup.find_all("table", class_="simpleTable simpleCreditsTable")
                ep_director = director_and_writers[0].find("td", class_="name").findNext().text.strip()
                ep_writers = []
                for person in director_and_writers[1].find_all("td", class_="name"):
                    ep_writers.append(person.findNext().text.strip() + " " + person.findNext("td", class_="credit").text.strip())
                characters = []
                for group in ep_soup.find_all("td", class_="character"):
                    for _ in group.find_all("a"):
                        characters.append(_.text)           
                inner_dict["Director"] = ep_director
                inner_dict["Writers"] = ep_writers
                inner_dict["Characters"] = characters
                time.sleep(3.7)

                season_dict[ep_name] = inner_dict
            
        all_simpsons_data["Season {}".format(str(season))] = season_dict
        time.sleep(6)
    
    list_of_dfs = [pd.DataFrame.from_dict(all_simpsons_data["Season {}".format(i)], orient="index") for i in range(1, (len(seasons) + 1))]
    everything = pd.concat(list_of_dfs)
    
    return everything

# For getting plots from Wikisimpsons (didn't end up using)
def get_plots():
    
    ua = UserAgent()
    user_agent = {'User-agent': ua.random}
    plot_dict = {}
    
    for key, value in dict_of_season23_links.items():
        url = value
        response = requests.get(url, headers=user_agent)
        print("'{}' request status code: {}".format(key, str(response.status_code)))
        page = response.text
        soup = BeautifulSoup(page)
        
        plot = []
        a = test_soup.find("span", class_="mw-headline", id="Plot").findNext("p")
        plot.append(a.text)
        b = a.find_next_sibling()
        while b.name != "h2" and b.name != "table":
            plot.append(b.text)
            b = b.find_next_sibling()
        plot_dict[key] = plot
        time.sleep(6.1)
    
    return plot_dict

# For getting dialogue percentages for characters
def percentage_of_ep(episode_num):
    '''Takes an episode number as int (episode_num) and returns a datafame containing 
    each character's word count in that episode and percentage of the whole episode
    and total minutes.
    
    Arguments: int
    Returns: dataframe
    '''
    line_breakdown = dialogue_lines[dialogue_lines["Episode number"] == episode_num]
    line_breakdown["Word count"] = line_breakdown["Word count"].astype(int)
    total_words = line_breakdown["Word count"].sum()
    
    new_df = line_breakdown.groupby("Character")["Word count"].sum().reset_index()
    new_df["Share of episode (%)"] = new_df["Word count"].apply(lambda x: (x*100)/total_words)
    new_df["Share of episode (mins)"] = new_df["Share of episode (%)"].apply(lambda x: (x*26)/100)
    new_df["Character"] = new_df["Character"].str.title()
    
    return new_df

# For getting dialogue percentages for specific characters

def homer_series():
    homer_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            homer_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                percentage = df.loc[df["Character"] == "Homer Simpson"].iloc[0][2]
                if percentage > 0 and percentage < 1:
                    homer_percentage.append(np.nan)
                else:
                    homer_percentage.append(percentage)
            except ValueError:
                homer_percentage.append(np.nan)
    return homer_percentage

def bart_series():
    bart_percentage = []
    for i in range(1, 569):
        print(i)
        if i in [424, 441, 447, 550]:
            bart_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Bart Simpson" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Bart Simpson"].iloc[0][2]
                    bart_percentage.append(percentage)
                else:
                    bart_percentage.append(0)
            except ValueError:
                bart_percentage.append(np.nan)
    return bart_percentage

def lisa_series():
    lisa_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            lisa_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Lisa Simpson" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Lisa Simpson"].iloc[0][2]
                    lisa_percentage.append(percentage)
                else:
                    lisa_percentage.append(0)
            except ValueError:
                lisa_percentage.append(np.nan)
    return lisa_percentage

def marge_series():
    marge_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            marge_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Marge Simpson" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Marge Simpson"].iloc[0][2]
                    marge_percentage.append(percentage)
                else:
                    marge_percentage.append(0)
            except ValueError:
                marge_percentage.append(np.nan)
    return marge_percentage

def moe_series():
    moe_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            moe_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Moe Szyslak" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Moe Szyslak"].iloc[0][2]
                    moe_percentage.append(percentage)
                else:
                    moe_percentage.append(0)
            except ValueError:
                moe_percentage.append(np.nan)
    return moe_percentage

def milhouse_series():
    milhouse_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            milhouse_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Milhouse Van Houten" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Milhouse Van Houten"].iloc[0][2]
                    milhouse_percentage.append(percentage)
                else:
                    milhouse_percentage.append(0)
            except ValueError:
                milhouse_percentage.append(np.nan)
    return milhouse_percentage

def mrburns_series():
    mrburns_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            mrburns_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "C. Montgomery Burns" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "C. Montgomery Burns"].iloc[0][2]
                    mrburns_percentage.append(percentage)
                else:
                    mrburns_percentage.append(0)
            except ValueError:
                mrburns_percentage.append(np.nan)
    return mrburns_percentage

def grampa_series():
    grampa_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            grampa_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Grampa Simpson" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Grampa Simpson"].iloc[0][2]
                    grampa_percentage.append(percentage)
                else:
                    grampa_percentage.append(0)
            except ValueError:
                grampa_percentage.append(np.nan)
    return grampa_percentage

def flanders_series():
    flanders_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            flanders_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Ned Flanders" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Ned Flanders"].iloc[0][2]
                    flanders_percentage.append(percentage)
                else:
                    flanders_percentage.append(0)
            except ValueError:
                flanders_percentage.append(np.nan)
    return flanders_percentage

def skinner_series():
    skinner_percentage = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            skinner_percentage.append(np.nan)
        else:
            try:
                df = percentage_of_ep(i)
                if "Seymour Skinner" in list(df["Character"]):
                    percentage = df.loc[df["Character"] == "Seymour Skinner"].iloc[0][2]
                    skinner_percentage.append(percentage)
                else:
                    skinner_percentage.append(0)
            except ValueError:
                skinner_percentage.append(np.nan)
    return skinner_percentage

# For getting guest stars from TVDB
def guest_stars(season_list):
    '''Takes a list of season numbers as ints (season_list) and returns a list of guest stars
    appearing in every episode of those seasons.
    Arguments: list of ints
    Returns: list of lists
    '''
    all_guest_stars = []
    for i in range(len(season_list)):
        link = list_of_tvdb_links[i]
        season_response = requests.get(link, headers=user_agent)
        print(season_response.status_code)
        season_page = season_response.text
        season_soup = BeautifulSoup(season_page)
        link_table = season_soup.find("tbody").find_all("a")
        season_urls = ["https://www.thetvdb.com{}".format(link["href"]) for link in link_table]
        for url in season_urls:
            response = requests.get(url, headers=user_agent)
            print(url, response.status_code)
            ep_page = response.text
            ep_soup = BeautifulSoup(ep_page)
            cast_table = ep_soup.find("tbody")
            if cast_table != None:
                cast = cast_table.find_all("tr")
                guest_stars = []
                for person in cast:
                    if person.find_all("td")[1].text.strip() == "Guest Star":
                        guest_stars.append(person.find_all("td")[0].text.strip())
                if len(guest_stars) == 0:
                    guest_stars.append([])
            else:
                guest_stars.append([])
            all_guest_stars.append(guest_stars)
            time.sleep(3)
    
    return all_guest_stars

# For getting IMDB ratings data/demographic data
def get_imdb_ratings_info(seasons):
    '''
    Arguments: A list of season numbers (ints)
    Returns: A dict of data for every season
    '''
    
    all_ratings_data = {}
    
    for season in seasons:
        ua = UserAgent()
        user_agent = {'User-agent': ua.random}
        url = "https://www.imdb.com/title/tt0096697/episodes?season={}".format(str(season))
        response = requests.get(url, headers=user_agent)
        print("Season {} request status code: {}".format(str(season), str(response.status_code)))
        page = response.text
        simp_soup = BeautifulSoup(page)
        
        season_eps = simp_soup.find("div", class_="list detail eplist").find_all("div", class_=re.compile("^(list_item )(odd|even)$"))
        season_dict = {}
        
        for i, episode in enumerate(season_eps):
            ep_details = episode.find("div", class_="info")
            ep_name = ep_details.find("a", itemprop="name").text
            inner_dict = {}
                       
            if season <= 30:  
                url_part = episode.find("a", itemprop="name")["href"]
                ep_url = "https://www.imdb.com{}{}".format(url_part[:17], "ratings")
                ep_response = requests.get(ep_url, headers=user_agent)
                print("Season {} Episode {} request status code: {}".format(str(season), str(i+1), str(ep_response.status_code)))
                ep_page = ep_response.text
                ep_soup = BeautifulSoup(ep_page)

                main = ep_soup.find("div", id="main")
                ratings_tables = main.find_all("table")
                ratings_dict = {}
                for score in ratings_tables[0].find_all("tr")[1:11]:
                    sections = score.find_all("td")
                    rating = sections[0].find("div", class_="rightAligned").text
                    votes = sections[2].find("div", class_="leftAligned").text
                    ratings_dict[rating] = votes
                groups = ratings_tables[1].find_all("tr")
                group_names = groups[0].find_all("th", class_="firstTable")
                brackets = []
                for name in group_names:
                    bracket = name.find("div", class_="tableHeadings").text
                    brackets.append(bracket)
                bracket_dict = {}
                for row in groups[1:]:
                    segment_dict = {} 
                    td = row.find_all("td")
                    segment = td[0].find("div", class_="leftAligned").text.strip()
                    segment_dict = {}
                    segment_list = []
                    for i, cell in enumerate(td[1:]):
                        score = cell.find("div", class_="bigcell").text.strip()
                        number_parent = cell.find_next("div", class_="smallcell")
                        number = number_parent.find("a").text.strip()
                        segment_dict[brackets[i]] = [score, number]
                    bracket_dict[segment] = segment_dict
                season_dict[ep_name] = [ratings_dict, bracket_dict]
                time.sleep(3.7)
            
            else:
                url_part = episode.find("a", itemprop="name")["href"]
                ep_url = "https://www.imdb.com{}{}".format(url_part[:18], "fullcredits")
                ep_response = requests.get(ep_url, headers=user_agent)
                print("Season {} Episode {} request status code: {}".format(str(season), str(i+1), str(ep_response.status_code)))
                ep_page = ep_response.text
                ep_soup = BeautifulSoup(ep_page)

                main = ep_soup.find("div", id="main")
                ratings_tables = main.find_all("table")
                ratings_dict = {}
                for score in ratings_tables[0].find_all("tr")[1:11]:
                    sections = score.find_all("td")
                    rating = sections[0].find("div", class_="rightAligned").text
                    votes = sections[2].find("div", class_="leftAligned").text
                    ratings_dict[rating] = votes
                groups = ratings_tables[1].find_all("tr")
                group_names = groups[0].find_all("th", class_="firstTable")
                brackets = []
                for name in group_names:
                    bracket = name.find("div", class_="tableHeadings").text
                    brackets.append(bracket)
                bracket_dict = {}
                for row in groups[1:]:
                    segment_dict = {} 
                    td = row.find_all("td")
                    segment = td[0].find("div", class_="leftAligned").text.strip()
                    segment_dict = {}
                    segment_list = []
                    for i, cell in enumerate(td[1:]):
                        score = cell.find("div", class_="bigcell").text.strip()
                        number_parent = cell.find_next("div", class_="smallcell")
                        number = number_parent.find("a").text.strip()
                        segment_dict[brackets[i]] = [score, number]
                    bracket_dict[segment] = segment_dict
                season_dict[ep_name] = [ratings_dict, bracket_dict]
                time.sleep(3.7)
            
        all_ratings_data["Season {}".format(str(season))] = season_dict
        time.sleep(3.4)
        with open("ratings.pickle", "wb") as to_write:
            pickle.dump(all_ratings_data, to_write)
        print("Just pickled!")
    
    return all_ratings_data

### For making columns from scraped IMDB demographic data
def make_rater_columns(list_of_age_groups):
    
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    
    for episode in list_of_age_groups:
        list1.append(episode["All Ages"])
        list2.append(episode["<18"])
        list3.append(episode["18-29"])
        list4.append(episode["30-44"])
        list5.append(episode["45+"])

    return list1, list2, list3, list4, list5


# For determining whether the character with the most dialogue in an episode is one of 
# the main four characters: Homer, Marge, Bart, and Lisa
def main_or_side():
    
    main_4_or_not = []
    most_words_list = []
    for i in range(1, 569):
        if i in [424, 441, 447, 550]:
            main_4_or_not.append(np.nan)
            most_words_list.append(np.nan)
        else:
            df = percentage_of_ep(i)
            most_words = list(df[(df["Share of episode (%)"] \
                  == df["Share of episode (%)"].max())]["Character"])[0]
            most_words_list.append(most_words)
            print(i, most_words)
            if most_words in ["Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson"]:
                main_4_or_not.append(1)
            else:
                main_4_or_not.append(0)
                
    return most_words_list, main_4_or_not