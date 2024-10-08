from bs4 import BeautifulSoup
import requests
import pandas as pd


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
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        doc = BeautifulSoup(result.text, 'html.parser')
        return doc
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the HTML from the URL: {e}")
        return None


def get_jobs_on_page(page):
    """This returns the BeautifulSoup object that contains all the jobs on a page"""
    try:
        job_div = page.find("ul", {"id": "job-list"})
        job_href = job_div.find_all(class_="chakra-button css-27ga1i")
        return job_href
    except AttributeError as e:
        print(f"Error finding jobs on the page: {e}")
        return []


def get_job_dict(job_url):
    """This function returns a dictionary of the job details."""
    try:
        job_links = 'https://www.workopolis.com' + job_url['href']
        job_html = get_html(job_links)
        if job_html is None:
            return {}

        job_title = job_html.find(
            'h1', {"class": "chakra-heading css-yvgnf2"}).text
        job_company = job_html.find(
            'span', {"data-testid": "viewJobCompanyName"}).text
        job_location = job_html.find(
            'span', {"data-testid": "viewJobCompanyLocation"}).text
        skills_div = job_html.find(class_="chakra-wrap__list css-19lo6pj")
        skills_tag = skills_div.find_all(
            "span", {"data-testid": "viewJobQualificationItem"}
        ) if skills_div else None
        skills = ", ".join(
            [skill.text for skill in skills_tag]) if skills_tag else None

        details = {
            "title": job_title.strip(),
            "company": job_company.strip(),
            "location": job_location.strip(),
            "link": job_links,
            "skills": skills.strip() if skills else None,
        }
        return details
    except Exception as e:
        print(f"Error processing job details: {e}")
        return {
            "title": "",
            "company": "",
            "location": "",
            "link": "",
            "skills": "",
        }


def main():
    print()
    welcome = "Welcome to Job Listing Analyzer"
    print(welcome)
    print("=" * len(welcome))
    print()

    title = input("Enter your desired job title, skill, or company: ")
    city = input("Enter your desired location, province, or remote: ")

    print("Searching for jobs online for you")
    print()
    print("+" * 15)

    doc = get_html(get_job_url(title, city))
    if doc is None:
        print("Failed to retrieve jobs. Please try again later.")
        return

    try:
        jobs_available = doc.find(
            'div', {"data-testid": "headerSerpJobCount"}
        ).find('p', {"class": "css-gu0het"}).text
    except AttributeError as e:
        print(f"Error finding the total number of jobs available: {e}")
        return

    jobs_found = []
    data = {
        'job_title': [],
        'company': [],
        'location': [],
        'link': [],
        'skills': [],
    }

    count = 0
    while True:
        page_nav = doc.find(
            "nav", {"role": "navigation", "class": "css-1hog1e3"})
        jobs = get_jobs_on_page(doc)
        if not jobs:
            break

        for job in jobs:
            count += 1
            job_found = get_job_dict(job)
            if not job_found.get('title'):
                continue

            jobs_found.append(job_found)
            data['job_title'].append(job_found['title'])
            data['company'].append(job_found['company'])
            data['location'].append(job_found['location'])
            data['skills'].append(job_found['skills'])
            data["link"].append(job_found['link'])

            print()
            print(job_found['title'])
            print(job_found['company'])
            print(job_found['location'])
            print(job_found['skills'])
            print(job_found['link'])
            print('-' * 10)
            print()
            print(f"{count} of {int(jobs_available)} found")
            print()
            print('=' * 10)

        next_page = page_nav.find(
            "a", {"aria-label": "Next page"}) if page_nav else None
        if next_page:
            doc = get_html(next_page['href'])
            if doc is None:
                print("Failed to load the next page. Stopping the search.")
                break
        else:
            break

        if len(jobs_found) >= int(jobs_available):
            break

    if jobs_found:
        df = pd.DataFrame(data)
        # Export csv file
        title_striped = title.replace(" ", "_")
        city_stripped = city.replace(" ", "_")
        file_name = f"{title_striped}_{city_stripped}.csv"
        df.to_csv(file_name, index=False)
        print()
        print("+" * 15)
        print(f"Exported jobs found as csv file ({file_name})")
    else:
        print("No jobs found.")


if __name__ == "__main__":
    main()
