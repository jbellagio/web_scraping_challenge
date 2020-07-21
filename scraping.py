import pandas as pd
from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser
import requests
import time
import re

# Create scrape function
def scrape():

    executable_path ={'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_p = mars_news(browser)

    # run functions and store in dict for html later

    output = {
        "news_title": news_title,
        "news_p":news_p,
        "featured_img":featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": weather(browser),
        "facts": facts(),
    }
    return output

# moved code from jupyter notebook to here
def featured_image(browser):

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    find_elem2 = browser.find_by_id('full_image')
    find_elem2.click()

    browser.is_element_present_by_text('more info', wait_time=1)
    find_elem3 = browser.find_link_by_partial_text('more info')
    find_elem3.click()

    html = browser.html
    soup1 = bs(html, 'html.parser')

    image_url = soup1.select_one('figure.lede a img').get("src")

    featured_image_url  = "https://www.jpl.nasa.gov" + image_url
    return image_url

def weather(browser):

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup2 = bs(hmtl, "html.parser")

    mars_tweet = soup2.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    try:
        weather = mars_tweet.find('p', "tweet-text").get_text()
    except AttributeError:
        pattern = re.compile(r'sol')
        weather = soup2.find('span', text=pattern).text
        
    return weather

def hemispheres(browser):

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    urls = browser.find_by_css("a.product-item h3")

    for i in range(len(urls)):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[i].click()
    
        find_element3 = browser.find_link_by_text('Sample').first
        hemisphere['img_url']= find_element3['href']
    
        hemisphere['title'] = browser.find_by_css("h2.title").text
    
        hemisphere_image_urls.append(hemisphere)
    
        browser.back()
    
    return hemisphere_image_urls

def facts():

    mars_df = pd.read_html('https://space-facts.com/mars/')[0]
    mars_df.columns = ["Question", "Answer"]
    mars_df.set_index("Question", inplace=True)

    return df.to_html(classes="table")


def news():

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup3 = bs(html, 'html.parser')
    find_element = soup3.select_one('ul.item_list li.slide')

    find_element.find("div", class_='content_title')

    news_title = find_element.find("div", class_="content_title").get_text()

    news_p = find_element.find("div", class_="article_teaser_body").get_text()

    return news_title, news_p

if __name__ == "__main__":
    print(scrape())
