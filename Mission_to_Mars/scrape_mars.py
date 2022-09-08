# Import Libraries
from tracemalloc import Statistic
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import time





def scrape():
    returnDict = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News Scrape
    #URL of page to be scraped
    marsNewsURL = 'https://redplanetscience.com/'
    browser.visit(marsNewsURL)

    # Create Beautiul Soup Object then parse
    newsHtml = browser.html
    soup = BeautifulSoup(newsHtml, 'html.parser')
   

    #scrape latest headline ***OUTPUT***
    newsHeadline = soup.find('div', class_='content_title').text.strip()
    returnDict["news_title"] = newsHeadline
    newsTeaser = soup.find('div', class_='article_teaser_body').text.strip()
    returnDict["news_para"] = newsTeaser
    #print(newsHeadline)
    #print(newsTeaser)

    browser.quit()

    #JPL Mars Space Images—Featured Image
    #URL of page to be scraped
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    urlImage = 'https://spaceimages-mars.com/'
    browser.visit(urlImage)

    #Time page to load and click full image using webdriver
    time.sleep(2)
    browser.links.find_by_partial_text('FULL IMAGE').click()

    #Set up Beautiful Soup
    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')

    #Parse soup, extract image endpoint and create variable to store URL ***OUTPUT***
    image_box = soup1.find('div', class_='fancybox-inner')
    featured_image_url = urlImage.replace('index.html', '') + image_box.img['src']
    featured_image_url

    returnDict["mars_image"] = featured_image_url

    browser.quit()

    #Mars Facts
    # Set up URL to be scraped
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    urlFacts = 'https://galaxyfacts-mars.com/'
    browser.visit(urlFacts)

    
    #tableList = []
    #tableDict = {}
    
    # Create BS and parse
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    #Source table
    tables = pd.read_html(urlFacts)

    #Convert to DF
    df_Mars_facts = tables[0]
    df_Mars_facts.columns = ['Statistic', 'Mars', 'Earth']
    df_Mars_facts.set_index('Statistic', inplace=True)

    #mars_fact_df.to_html()
    with open('mars_facts_df.html', 'w', encoding='utf-8') as fo:
        df_Mars_facts.to_html(fo)

    #df_Mars_facts.columns =df_Mars_facts.iloc[0]
    #df_Mars_facts = df_Mars_facts.drop([0])

    #Convert to html ***OUTPUT***
    #tableDict['Mars_Earth_Data'] = df_Mars_facts.to_html()
    #tableList.append(tableDict)

    returnDict["mars_earth"] = df_Mars_facts

    browser.quit()

    #Mars Hemispheres  

    #URL of page to be scraped
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    urlHemi = 'https://marshemispheres.com/'
    browser.visit(urlHemi)

    links = browser.find_by_css("a.product-item img")
    #print (links)
    totalLinks = range(len(links))

    #Create List ***OUTPUT***
    marsHemi = []
        
    #For loop to collect image titles and urls
    for index in totalLinks:
        hemispheres = {}
        browser.find_by_css("a.product-item img")[index].click()
    
        title_text = browser.find_by_css("h2.title").text
        mars_image = browser.links.find_by_text("Sample").first["href"]
        hemispheres["title"] = title_text
        hemispheres["image_url"] = mars_image
        marsHemi.append(hemispheres)
        
        browser.back()
    returnDict["mars_hemis"] = marsHemi
    
    browser.quit()
    
    return(returnDict)

    





