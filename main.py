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


def get_job_url(title: str, city: str) -> str:
    """This gets the user input and returns a url to the main page"""
    title = title.replace(" ", "+")
    city = city.replace(" ", "+")
    url = f"https://www.workopolis.com/search?q={title}&l={city}"
    return url


def get_html(url):
    """This parses the html from the url entered."""
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


def get_jobs_on_page(page):
    """
    This returns the Beatifulsoup dict that contains all the job on a page"""
    job_div = page.find("ul", {"id": "job-list"})
    job_href = job_div.find_all(class_="chakra-button css-27ga1i")
    return job_href


def get_job_dict(job_url):
    """
    This function returns a dictionary of the job details.
    """
    job_links = 'https://www.workopolis.com' + job_url['href']
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


doc = get_html(get_job_url(title, city))
jobs_found = []

while True:
    page_nav = doc.find("nav", {"role": "navigation", "class": "css-1hog1e3"})
    jobs = get_jobs_on_page(doc)
    for job in jobs:
        job_found = get_job_dict(job)
        jobs_found.append(job_found)
        print(job_found)
    next_page = page_nav.find("a", {"aria-label": "Next page"})
    if next_page:
        doc = get_html(next_page['href'])
    else:
        break
    if len(jobs_found) >= 1000:
        break
