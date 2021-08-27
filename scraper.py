from bs4 import BeautifulSoup
import csv
import requests
import re
import pandas as pd

file = open('plumber_data_final.csv', 'w')
writer = csv.writer(file)
writer.writerow(['Company Name', 'Company Location', 'Company e-mail', 'Company website', 'Company office phone', 'Company mobile phone', 'Page'])
companies_list = []
locations_list = []
mobiles_list = []
offices_list = []
emails_list = []
websites_list = []
page_numbers_list = []
    
for i in range (1,14):
    page_number = i
    with open(f'C:/Users/Nawfel/Desktop/web_scraping/plumber_htmls/MPAQ - Find a plumber ({page_number}).html', 'r', encoding='utf-8') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')

    # Company Name
    comp = soup.find_all('div', class_ = 'search-result-location')
    
    for company in comp:
        companies_list.append(company.findChild().getText())

    # Company Location
    loc = soup.find_all('div', class_ = 'search-result-location')
    
    for location in loc:
        locations_list.append(location.findChildren()[1].getText())

    # Company Mobile Phone
    mobiles = soup.find_all('div', class_ = 'search-result-profile small-12 medium-5 columns')

    for mobile in mobiles:
        if '@' in mobile.findChildren()[3].getText():
            mobiles_list.append('N/A')
        else:
            mobiles_list.append(mobile.findChildren()[3].getText())

    # Company Office Phone
    office_phones = soup.find_all('div', class_ = 'search-result-profile small-12 medium-5 columns')
    
    for office in office_phones:
        offices_list.append(office.findChildren()[5].getText())

    for i in range(0,len(offices_list)):
        if '04' not in offices_list[i]:
            offices_list[i] = 'N/A'

    # Company Email
    emails = soup.find_all('a', href = re.compile("^mailto:"))
    
    for email in emails:
        emails_list.append(email.getText())

    #Company WebSite
    divs = soup.find_all('div', class_ = 'search-result-profile small-12 medium-5 columns')
    
    for div in divs:
        if ('www' in div.getText()) | ('http' in div.getText()) | ('brisbaneplumber.com' in div.getText()) | ('trentscottsplumbing' in div.getText()):
            websites = div.find_all('a', href = re.compile("^http"))
            for website in websites:
                websites_list.append(website.getText())
        else:
            websites_list.append('N/A')
    
    #Company page number
    for j in range(0,10):
        page_numbers_list.append(page_number)
            

for i in range(0,126):
    writer.writerow([companies_list[i], locations_list[i], emails_list[i], websites_list[i], offices_list[i], mobiles_list[i], page_numbers_list[i]])

print("File successfully created !")

file.close()
