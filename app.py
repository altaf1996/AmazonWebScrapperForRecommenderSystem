"""
1) First start the amazon website.
2) Go to Search bar and search for a product you want.
3) Product page will be displayed scroll down and Click on  "see all reviews"
4) Copy the url for "see all reviews" Page
5) pass the copied url to a create_df() function
6) Run the function u will get the DataFrame of (review_title, reviews_date, reviews_ratings, reviews_comment & reviews_name )
"""

#import the requested library
import requests                                 
import pandas as pd                            
from bs4 import BeautifulSoup as bs

# url to scrap
url = "https://www.amazon.in/Panasonic-DMC-G7KGW-K-Mirrorless-Camera-Black/product-reviews/B07JLXC5BR?pageNumber=1&reviewerType=all_reviews"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'} #headers

#creatre a function which loads a html page
def get_page(url):
  r = requests.get(url, headers=headers)  #request to the url for html page
  soup = bs(r.text, 'html.parser')        #getting content fro html page
  return soup                             #returns the soup object

#create a function to find a next page
def getnextpage(soup):
  page = soup.find('ul', {'class':'a-pagination'}) 
  if not page.find('li', {'class':'a-disabled a-last'}):
    url = 'https://www.amazon.in' + str(soup.find('li', {'class': 'a-last'}).find('a')['href']) #creating url for next page
    return url
  else:
    return

#create a function for getting relevant data
def reviews(soup):
  review = soup.find_all('div', {'data-hook':'review'})
  review_title =   []   #title from reviews page
  review_name =    []   #name from reviews page 
  review_date =    []   #date from review page
  review_rating =  []   #rating from review page
  review_comment = []   #comment from review page
  for item in review:
    review_title.append(item.find('a', {'data-hook':'review-title'}).text.strip())        # review
    review_name.append(item.find('div', {'class': 'a-profile-content'}).text.strip())     # name
    review_date.append(item.find('span', {'data-hook': 'review-date'}).text.replace("Reviewed in India on", "").strip()) # date  
    review_rating.append(item.find('i', {'data-hook':'review-star-rating'}).text.replace("out of 5 stars","").strip()) # rating
    review_comment.append(item.find('span', {'data-hook':'review-body'}).text.strip()) # comment
  return review_title, review_name, review_date, review_rating, review_comment 

# Crea a function to add data into empty lists
def get_data(url):
  ti = []
  na = []
  da = []
  ra = []
  co = []
  while True:
    soup = get_page(url)
    url = getnextpage(soup)
    title, name, date, rating, comment = reviews(soup)
    for i in title:
      ti.append(i)
    for n in name:
        na.append(n)
    for d in date:
      da.append(d)
    for r in rating:
      ra.append(r)
    for c in comment:
      co.append(c)
    
    if not url:
      break
    print(url)
  return ti,na, da, ra, co

# create a function for converting a list into DataFrame
def create_df(url):
  ti, na, da, ra, co = get_data(url)
  datas = pd.DataFrame(columns=['title', 'name', 'date', 'rating', 'comment'])
  datas["title"] = ti
  datas["name"] = na
  datas["date"] = da
  datas["rating"] = ra
  datas["comment"] = co
  return datas

df = create_df(url=url)
print(df.head())