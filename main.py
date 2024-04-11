from bs4 import BeautifulSoup
import requests
import re

print()
welcome = "Welcome to Job analyzer"
print(welcome)
print("=" * len(welcome))
print()

title = input("Enter your desired job title: ")
city = input("Enter your desired location: ")


def get_job_url(title, city):
    title = title.replace(" ", "+")
    city = city.replace(" ", "+")
    url = f"https://www.workopolis.com/search?q={title}&l={city}"
    return url


def get_html(url):
    headers = {
        "Dnt": "1",
        "Referer": "https://www.workopolis.com/search?q=front+end+developer&l=toronto",
        "Sec-Ch-Ua": "\"Chromium\";v=\"123\", \"Not:A-Brand\";v=\"8\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    result = requests.get(url, headers=headers).text
    doc = BeautifulSoup(result, 'html.parser')
    return doc


doc = get_html(get_job_url(title, city))
total_job = int(doc.find(class_="chakra-text css-gu0het").text)
job_div = doc.find("ul", {"id": "job-list"})
job_href = job_div.find_all(class_="chakra-button css-27ga1i")
page_nav = doc.find("nav", {"role": "navigation", "class": "css-1hog1e3"})
page_nav_link = page_nav.find_all("a", {"class": "chakra-link css-kqypvt"})
next_page = page_nav.find("a", {"aria-label": "Next page"})
# print(next_page)

for page in page_nav_link:
    pass
    # print(page)
# print(total_job)


def get_job_dict(url: dict) -> dict:
    job_links = 'https://www.workopolis.com' + url['href']
    job_html = get_html(job_links)
    job_title = job_html.find('h1', {"class": "chakra-heading css-yvgnf2"}).text
    job_company = job_html.find('span', {"data-testid": "viewJobCompanyName"}).text
    job_location = job_html.find(
        'span', {"data-testid": "viewJobCompanyLocation"}
    ).text
    job_detail = job_html.find('span', {"data-testid": "detailText"}).text
    skills_div = job_html.find(class_="chakra-wrap__list css-19lo6pj")
    skills_tag = skills_div.find_all(
        "span", {"data-testid": "viewJobQualificationItem"}
    ) if skills_div else None
    skills = ", ".join([skill.text for skill in skills_tag]) if skills_tag else None

    details = {
        "title": job_title.strip(),
        "company": job_company.strip(),
        "location": job_location.strip(),
        "details": job_detail.strip(),
        "skills": skills.strip() if skills else None,
        "link": job_links
    }

    return details


for job in job_href:
    print(get_job_dict(job))
