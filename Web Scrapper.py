from selenium import webdriver 
from selenium.common.exceptions import ElementNotVisibleException
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()
# Tshirts and tank tops--
products=[] #List to store name of the product
price_original=[] #List to store price of the product
price_Sale = []
article_code =[] #List to store rating of the product
article_category = []
article_color = []
blank_link= {}

#############>>>
website_link = "link-to-website"
driver.get(website_link)
sleep(0.1)
driver.find_element_by_class_name('js-read-gdpr').click()
m=0

while True:
    try:
        driver.find_element_by_class_name('js-load-more').click()
        sleep(3)

    except ElementNotVisibleException:
        break


content = driver.page_source
soup = BeautifulSoup(content)
driver.close()

#############>>>
with open("/Users/av.txt", "w") as text_file:
    text_file.write("Purchase Amount: %s" % content)


for a in soup.findAll('li', attrs={'class':'product-item'}):
    print("Product No- ", m)
    m=m+1
    name=a.find('h3', attrs={'class':'item-heading'})
    Oprice = a.find('span', attrs={'class':'price regular'}) 
    Sprice=a.find('span', attrs={'class':'price sale'})
    
    ARTICLEDATA = a.find('article', attrs={'class':'hm-product-item'})
    data_category = ARTICLEDATA['data-category']

    print('----------------')
    alink = a.find('a').get('href')
    link = 'https://www2.link.com/'+alink
    driver2.get(link)
    sleep(0.5)
    try:
        driver2.find_element_by_class_name('js-read-gdpr').click()
    except:
        pass
    
    pagesource = driver2.page_source

    internel_soup=BeautifulSoup(pagesource)
    n=0
    for j in internel_soup.findAll('ul',attrs = {'class':'inputlist clearfix'}):
        for i in j.findAll('li', attrs = {'class':'list-item'}):
            try:
                n=n+1
                print('Article No- ', n)
                articledata = i.find('a', attrs = {'class':'filter-option miniature'}) or i.find('a', attrs = {'class':'filter-option miniature active'})  
                articlecode = articledata['data-articlecode']
                articlecolor = articledata['data-color']
                article_code.append(articlecode)
                print(articlecode)
                article_color.append(articlecolor)
                print(articlecolor)
                products.append(name.text)
                print(name.text)
                price_original.append(Oprice.text)
                print(Oprice.text)
                price_Sale.append(Sprice.text)
                print(Sprice.text)
                article_category.append(data_category)
                print(data_category)
            except:
                blank_link[link]=n
                pass



#############>>>
SALE_MEN_HM = pd.DataFrame(
    {'Product Name': products,
     'Original Price': price_original,
     'Sale Price': price_Sale,
     'Option_Code': article_code,
     'Category': article_category,
     'Color' : article_color
    })
SALE_MEN_HM.to_csv('/Users/AV.csv')





Duplicates_In_Data = SALE_MEN_HM[SALE_MEN_HM.duplicated()]
len(SALE_MEN_HM.Option_Code.unique())
duplicateRowsDF = SALE_MEN_HM[SALE_MEN_HM.duplicated(keep=False)]
Data_After_removing_duplicates = SALE_MEN_HM.drop_duplicates()
Data_After_removing_duplicates.to_csv('/Users/AV.csv')


