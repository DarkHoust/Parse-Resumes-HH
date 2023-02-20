from bs4 import BeautifulSoup
import requests
import re

def parseLink(link):
    html = requests.get(link, headers={'User-Agent': 'Custom'})
    soup = BeautifulSoup(html.text, 'html.parser')

    title = None
    for _ in soup.findAll('span', attrs={'class': 'resume-block__title-text', 'data-qa':'resume-block-title-position'}):
        title = _.text

    job = None
    for _ in soup.findAll('li', attrs={'class': 'resume-block__specialization'}):
        job = _.text

    salary = None
    for _ in soup.findAll('span', attrs={'class': 'resume-block__salary'}):
        salary = _.text

    if len(soup.findAll('span', attrs={'data-qa': 'resume-personal-age'})) != 0:
        age = soup.findAll('span', attrs={'data-qa': 'resume-personal-age'})[0].text
        age = "".join(i for i in age if i.isdigit())
    else:
        age = None

    experience_years = 0
    experience_months = 0
    for _ in soup.findAll('span', attrs={'class': 'resume-block__title-text resume-block__title-text_sub'}):
        if "Опыт" in _.text or "experience" in _.text:
            experience = re.findall(r'\b\d+\b', _.text)
            if len(experience) == 2:
                experience_years = experience[0]
                experience_months = experience[1]
            elif len(experience) == 1:
                experience_years = experience[0]
            else:
                break

    employment = None
    for _ in soup.findAll('div', attrs={'class' : 'resume-block-container'}):
        if "Employment" in _.text:
            employment = _.text.split('Employment: ')[1].split('Work schedule:')[0]
            break
        if "Занятость" in _.text:
            employment = _.text.split('Занятость: ')[1].split('График работы:')[0]
            break

    schedule = None
    for _ in soup.findAll('div', attrs={'class': 'resume-block-container'}):
        if "График" in _.text:
            schedule = _.text.split('График работы: ')[1]
            break
        elif "schedule" in _.text:
            schedule = _.text.split('schedule: ')[1]
            break

    if len(soup.findAll('span', attrs={'data-qa': 'resume-personal-gender'})) != 0:
        sex = soup.findAll('span', attrs={'data-qa': 'resume-personal-gender'})[0].text
        if "Male" in sex:
            sex = True
        else:
            sex = False
    else:
        sex = None

    resume = {
        'title' : title,
        'specialization' : job,
        'salary': salary,
        'age': age,
        'employment' : employment,
        'experience_years': experience_years,
        'experience_months': experience_months,
        'sex': sex,
        'link': link
    }

    return resume

def getLink(job):
    job.replace(" ", "+")
    list_links = []

    url = f"https://hh.kz/search/resume?text={job}&area=40&currency_code=KZT&no_magic=true&ored_clusters=true&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time"
    html = requests.get(url, headers={'User-Agent': 'Custom'})
    soup = BeautifulSoup(html.text, 'html.parser')

    try:
        pcounter = int(soup.find('div', attrs={'class': 'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    except AttributeError:
        for block in soup.findAll('a', attrs={'class': 'serp-item__title'}):
            link = "https://hh.kz" + block.get('href').split('?')[0]
            list_links.append(link)
            print(link)
            if len(list_links) >= 500:
                return list_links
        return list_links

    for _ in range(pcounter):
        url = f"https://hh.kz/search/resume?text={job}&area=40&currency_code=KZT&no_magic=true&ored_clusters=true&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&page={_}"
        html = requests.get(url, headers={'User-Agent': 'Custom'})
        soup = BeautifulSoup(html.text, 'html.parser')

        for i in soup.findAll('a', attrs={'class': 'serp-item__title'}):
            link = "https://hh.kz" + i.get('href').split('?')[0]
            list_links.append(link)
            if len(list_links) >= 500:
                return list_links

        return list_links


