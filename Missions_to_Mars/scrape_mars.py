import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager



def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    return browser 

def scrape():
    
    browser = init_browser()

    # Nasa Mars news
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(2)
    news_html = browser.html
    news_soup = bs(news_html,'lxml')
    news_title = news_soup.find("div", class_="list_text").find('a').get_text()
    news_p = news_soup.find("div", class_="article_teaser_body").get_text()


    # JPL Mars Space Images - Featured Image
    jurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jurl)
    time.sleep(2)
    jhtml = browser.html
    jpl_soup = bs(jhtml,"html.parser")
    image_url = jpl_soup.find('div', class_='sm:object-cover object-cover').find('img')['src']
    # base_link = "https:"+jpl_soup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    # feature_url = base_link+image_url
    featured_image_title = "Cydonia Colles - False Color"


    # Mars fact
    murl = 'https://space-facts.com/mars/'
    table = pd.read_html(murl)
    mars_df = table[0]
    mars_df.columns = ['Recordings', 'Measurements']
    mars_fact_html = mars_df.to_html(header=False, index=False)

    # Mars Hemispheres
    mhurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'},
        {"title": "Cerberus Hemisphere", "img_url": 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
        {"title": "Schiaparelli Hemisphere", "img_url": 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
        {"title": "Syrtis Major Hemisphere", "img_url": 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}
    ]
    
    
    # Close the browser after scraping
    browser.quit()



    # Return results
    mars_data ={
		'news_title' : news_title,
		'summary': news_p,
        'featured_image': image_url,
		'featured_image_title': featured_image_title,
		'fact_table': mars_fact_html,
		'hemisphere_image_urls': hemisphere_image_urls,
        'news_url': news_url,
        'jpl_url': jurl,
        'fact_url': murl,
        'hemisphere_url': mhurl,
        }
    return mars_data 

# collection.insert(mars_data)