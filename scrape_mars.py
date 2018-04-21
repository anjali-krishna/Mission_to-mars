import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    mars_data = {}


    # 1. Nasa Mars News
    url_nasa = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    content_title = soup.find('div', class_='content_title')
    news_title = content_title.text.strip()
    
    article_teaser_body = soup.find('div', class_='article_teaser_body')
    news_p = article_teaser_body.text.strip()

    # add to mars_data
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # 2. JPL Mars Space Images - Featured Image¶
    url_JPL = "https://www.jpl.nasa.gov/spaceimages/"
    browser.visit(url_JPL)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    find_image = soup2.find('a', class_='button fancybox')
    img_url = find_image['data-fancybox-href']
    
    featured_image_url = f'https://www.jpl.nasa.gov{img_url}'
    
    # add to mars_data
    mars_data["featured_image_url"] = featured_image_url
    
    # 3. Mars Weather
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    find_tweet = soup3.find('div', class_='js-tweet-text-container').text
    mars_weather = find_tweet.strip()
    
    # add to mars_data
    mars_data["mars_weather"] = mars_weather

    # 4. Mars Facts
    url_facts = "https://space-facts.com/mars/"

    tables = pd.read_html(url_facts)

    df = tables[0]

    table = df.to_html()

    # add to mars_data
    mars_data["table"] = table

    # 5. Mars Hemispheres
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url_hemispheres)

    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')

    one_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    two_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    three_url = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    four_url= 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    links = [one_url, two_url, three_url, four_url]

    titles = soup5.find_all('h3')
    
    titles_list = []
    for title in titles:
        titles_list.append(title.text)

    hemisphere_image_urls = [{'title': title,'img_url': link} for title, link in zip(titles_list,links)]

    # add to mars_data
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    # return mars_data dict
    print(mars_data["featured_image_url"])

    return mars_data
    
if __name__ == "__main__":
    scrape()
    