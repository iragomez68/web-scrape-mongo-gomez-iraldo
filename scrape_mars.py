# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def init_browser(headless):
    # @NOTE: Replace the path with your actual path to the chromedriver /usr/local/bin/
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=headless)

def visit_url(url, tag="body", class_="",headless=True):
    browser = init_browser(headless)
    browser.visit(url)
    html = browser.html
    
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'lxml')

    if class_:
        results = soup.find_all(tag, class_=class_)
    else:
        results = soup.find_all(tag)
    
    browser.quit()

    return results

def scrape_info():

    # URL of page to be scraped
    news_url = "https://mars.nasa.gov/news"
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    twiter_url = "https://twitter.com/marswxreport?lang=en"
    facts_url ="https://space-facts.com/mars/"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # mars news headline and paragraph from news_url
    nasa_results = visit_url(news_url, 'div','list_text')
    nasa_title = nasa_results[0].find('div', class_='content_title').a.text
    nasa_p = nasa_results[0].find('div', class_='article_teaser_body').text

    # mars feature image
    image_results = visit_url(img_url, "article","carousel_item")
    featured_image_url = "https://www.jpl.nasa.gov" + image_results[0].a["data-fancybox-href"]

    # mars weather
    twiter_results = visit_url(twiter_url, "p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = twiter_results[0].text.replace("hPapic.twitter.com/MhPPOHJg3m","")

    # mars facts
    fact_results = pd.read_html(facts_url)[1].rename(columns={0:'',1:'value'})
    fact_results.set_index('',inplace=True)
    mars_facts = fact_results.to_dict()

    # mars hemispheres images
    hemisphere_results = visit_url(hemisphere_url, "div", "description")
    hemisphere_baseurl = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = [{"title":hemisphere.h3.text, \
                            "img_url":visit_url(hemisphere_baseurl+hemisphere.a['href'], 'li')[0].a['href']}\
                            for hemisphere in hemisphere_results]
    
    mars_data = {
        "nasa_title" : nasa_title,
        "nasa_p" : nasa_p,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "mars_facts" : mars_facts,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    return mars_data