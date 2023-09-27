import requests  # http requests
from bs4 import BeautifulSoup  # Webscrape
import pandas as pd  # DF

# Skills & Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()


def extract(page, skill, place):
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36"}
    url = 'http://api.scraperapi.com?api_key=ad65b6043cbd9159e18a04cb9a0a05ea&url=https://in.indeed.com/jobs?q=' + skill + '&l=' + place + '&start={page}'
    r = requests.get(url, headers)

    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find(class_='jcs-JobTitle').text.strip()
        templink = item.find('a', {'class': 'jcs-JobTitle'}).get('href')
        link = f'https://in.indeed.com{templink}'
        company = item.find(class_='companyName').text.strip()
        try:
            rating = item.find('span', class_='ratingNumber').text.strip()
        except:
            rating = ''

        location = item.find('div', class_='companyLocation').text.strip()

        try:
            salary = item.find('div', class_='metadata salary-snippet-container').text.strip()
        except:
            salary = ''
        summary = item.find('div', class_='job-snippet').text.strip().replace('\n', '')
        date = item.find('span', class_='date').text.strip()

        job = {
            'title': title,
            'link': link,
            'company': company,
            'rating': rating,
            'location': location,
            'salary': salary,
            'summary': summary,
            'date': date
        }
        joblist.append(job)
    return


joblist = []
print("Relax this might take a while")


# main function
def do():
    for i in range(0, 40, 10):
        print(f'getting page,{i}')
        c = extract(i, skill, place)
        transform(c)

    df = pd.DataFrame(joblist)
    df.to_csv("jobs.csv")
    df.to_excel("jobs.xlsx", index=False)
    base_url = "https://api.telegram.org/bot5742639833:AAHySELaIbtlnKCt_aNN7pGXaEg-oBe3C8s/sendDocument"
    myFile = open("jobs.xlsx", "rb")
    parameters = {
        "chat_id": "661587899",
        "caption": "scrapped data"
    }

    files = {
        "document": myFile
    }
    resp = requests.get(base_url, data=parameters, files=files)
    print("Done!! Task completed")


do()