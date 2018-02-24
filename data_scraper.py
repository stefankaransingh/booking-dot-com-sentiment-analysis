# Web Automation Required Libraries
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Web Scraping Required Libraries
from bs4 import BeautifulSoup

FILE_NAME ='data.csv'

MAIN_URLS = [
    
"""https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhQiAEBmAEuuAEHyAEM2AEB6AEB-AELkgIBeagCAw&sid=b9a7c5c184a9aed184ff6f42e07df2ba&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.en-gb.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhQiAEBmAEuuAEHyAEM2AEB6AEB-AELkgIBeagCAw%3Bsid%3Db9a7c5c184a9aed184ff6f42e07df2ba%3Bcheckin_month%3D2%3Bcheckin_monthday%3D24%3Bcheckin_year%3D2018%3Bcheckout_month%3D2%3Bcheckout_monthday%3D25%3Bcheckout_year%3D2018%3Bclass_interval%3D1%3Bdest_id%3D-2601889%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bsrc%3Dindex%3Bsrc_elem%3Dsb%3Bss%3DLondon%252C%2520Greater%2520London%252C%2520United%2520Kingdom%3Bss_all%3D0%3Bss_raw%3DLond%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ss=London&ssne=London&ssne_untouched=London&city=-2601889&checkin_monthday=24&checkin_month=2&checkin_year=2018&checkout_monthday=25&checkout_month=2&checkout_year=2018&group_adults=2&group_children=0&no_rooms=1&from_sf=1""",
             
"""https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggJCAlhYSDNYBGhQiAEBmAEuuAEHyAEM2AEB6AEB-AELkgIBeagCAw&sid=b9a7c5c184a9aed184ff6f42e07df2ba&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.en-gb.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNYBGhQiAEBmAEuuAEHyAEM2AEB6AEB-AELkgIBeagCAw%3Bsid%3Db9a7c5c184a9aed184ff6f42e07df2ba%3Bcheckin_month%3D2%3Bcheckin_monthday%3D24%3Bcheckin_year%3D2018%3Bcheckout_month%3D2%3Bcheckout_monthday%3D25%3Bcheckout_year%3D2018%3Bcity%3D-2601889%3Bclass_interval%3D1%3Bdest_id%3D-2601889%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3DLondon%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3DLondon%3Bssne_untouched%3DLondon%26%3B&ss=new+york&ssne=London&ssne_untouched=London&city=-2601889&checkin_monthday=24&checkin_month=2&checkin_year=2018&checkout_monthday=25&checkout_month=2&checkout_year=2018&group_adults=2&group_children=0&no_rooms=1&from_sf=1&dest_id=&dest_type=&search_pageview_id=59ed8bd139920432&search_selected=false"""
            
]

def initialize_driver():
    #Initialize driver
    driver = webdriver.PhantomJS()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36""")
    
    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])
    driver.implicitly_wait(10)
    
    return driver


def get_urls(driver):
    tmp_url_list = []
    url_list = []
    for main_url in MAIN_URLS:
        driver.get(main_url)       
        for i in range(200):

            s = BeautifulSoup(driver.page_source,'html.parser')

            for link in s.find_all("a",{"class":"hotel_name_link url"},href=True):
                formatted_link = "https://www.booking.com"+link['href'][1:]
                if formatted_link not in tmp_url_list:
                    tmp_url_list.append(formatted_link)
            try:
                driver.find_elements_by_link_text('Next page')[0].click()
                driver.implicitly_wait(5)
            except:
                print('error occured on {0} click'.format(i))
                break
            
    print("No. of tmp urls ",str(len(tmp_url_list)))
    
    for i in range(len(tmp_url_list)):
        current_url = tmp_url_list[i]
        driver.get(current_url)
        driver.implicitly_wait(1)
        s = BeautifulSoup(driver.page_source,'html.parser')
        try:
            formatted_link  = 'https://www.booking.com'+s.find_all('a', {'class':'show_all_reviews_btn'},href=True)[0]['href']
            if formatted_link not in url_list:
                url_list.append(formatted_link)
        except:
            print("error occured for url: {0}".format(current_url))
            print('error occured on {0} click'.format(i))
    return url_list

def get_reviews(driver,url_list):
    reviews = {
        "pos":[],
        "neg":[]
    } 

    for url in url_list:
        driver.get(url)
        for i in range(250):
            s = BeautifulSoup(driver.page_source,'html.parser')
            for review in s.findAll("p", {"class": "review_neg"}):
                formatted_review = str(review).split('</i>')[1][:-4]
                if formatted_review not in reviews['neg']:
                    reviews['neg'].append(formatted_review)

            for review in s.findAll("p", {"class": "review_pos"}):
                formatted_review = str(review).split('</i>')[1][:-4]
                if formatted_review not in reviews['pos']:
                    reviews['pos'].append(formatted_review)
            try:
                driver.find_elements_by_link_text('Next page')[0].click()
                driver.implicitly_wait(5)
            except:
                print('error occured on {0} click'.format(i))
                break
    return reviews

def cleanse_data(review):
    if review.count('\n') > 0:
        review = review.replace('\n','')
    review = review[28:len(review)-7]
    return review

def write_to_file(reviews):
    with open(FILE_NAME,'w') as f:
        f.write('review||sentiment\n')
        for key in reviews.keys():
            for review in reviews[key]:
                review = cleanse_data(review)
                f.write(review+"||"+key+"\n") 
                
                
def main():
    print("initialize driver...")
    driver = initialize_driver()
    
    print("Getting urls..")
    url_list = get_urls(driver)
    print("Total No. of urls {0}".format(len(url_list)))
    
    print("Getting reviews for each url...")
    reviews = get_reviews(driver,url_list)
    
    print("Total No. of POS reviews {0}".format(len(reviews['pos'])))
    print("Total No. of NEG reviews {0}".format(len(reviews['neg'])))
    
    print("Writing to file..")
    write_to_file(reviews)
    
    print("Completed writing to file")
    
    
if __name__ == '__main__':
    main()