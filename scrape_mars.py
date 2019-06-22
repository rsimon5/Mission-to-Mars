from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd 
import time
import datetime

def scrape():

    mars=dict()

    mars_url = 'https://mars.nasa.gov/news/'
    response = requests.get(mars_url)

    soup = BeautifulSoup(response.text, 'lxml')
    try :
        news_title = soup.find("div", class_="content_title").text

        news_p = soup.find("div", class_="rollover_description_inner").text
        print("The news title is" + news_title)


        print("The text is" + news_p)


    except  AttributeError as Atterror:
        print(Atterror)

    mars["title"]=news_title
    mars["paragraph"]=news_p

    space_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(space_url)

    image = browser.find_by_id('full_image')
    image.click()

    time.sleep(2)
    link = browser.find_link_by_partial_text('more info')
    link.click()

    soup2 = BeautifulSoup(browser.html, 'html.parser')

    reference = soup2.find('figure', class_='lede')

    final_link=reference.a['href']
    featured_image_url='https://www.jpl.nasa.gov/' + final_link
    mars['featured_image_url']=featured_image_url

    print(featured_image_url)

    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    response3 = requests.get(twitter_url)
    soup3 = BeautifulSoup(response3.text, 'lxml')

    ##print(soup3.prettify())

    weather = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars["weather"]=weather

    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    mars_facts[0].rename(columns={0:"Type", 1: "Stat"}, inplace=True)

    marsdf = mars_facts[0]

    mars_html = marsdf.to_html()

    mars['html'] = mars_html

    mars_hem ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hem)

    soup5 = BeautifulSoup(browser.html, 'html.parser')

    class_collap_results = soup5.find('div', class_="collapsible results")

    items = soup5.find('div', class_="collapsible results").find_all('div',class_='item')

    List=list()
    image_urls = list()
    titles = list()
    for i in items:
        title = i.h3.text
        titles.append(title)
        href  = "https://astrogeology.usgs.gov" + i.find('a',class_='itemLink product-item')['href']
        browser.visit(href)
        time.sleep(10)
        soup6 = BeautifulSoup(browser.html, 'html.parser')
        urls = soup6.find('div', class_='downloads').find('li').a['href']
        image_urls.append(urls)

        hem_dict = dict()
        hem_dict['title'] = title
        hem_dict['img_url'] = urls
        List.append(hem_dict)
    
    mars['hemisphere_urls'] = List


    
    return mars

r = scrape()
print(r)