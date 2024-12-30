from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from src.models import user_persona, prompt, job_posting
from selenium import webdriver
import requests
import argparse
import re
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_profile_source(url='https://www.linkedin.com/in/antonio-castaldo/'):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # Create a browser instance
    driver = webdriver.Chrome(options=options)

    # Open the LinkedIn profile page
    driver.get(url)

    # Extract the page source or perform other actions with the browser
    source = driver.page_source

    # Close the browser
    driver.quit()

    return source

def scrape_profile(source):
    soup = BeautifulSoup(source, "html.parser")
    name = soup.find("title").text.strip().split('|')[0].split(',')[0].split('-')[0].strip()
    skills = "Guess the skills from the rest of the information"
    certificates_list = get_certificates(soup, source)
    educations_list = get_educations(soup, source)
    experiences_list = get_experiences(soup, source)
    return user_persona.UserPersona(name, educations_list, experiences_list, skills, certificates_list)


def get_certificates(soup, source):
    certificates_list = soup.find("section", class_="core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section certifications")
    certification_titles = certificates_list.find_all('h3', class_='profile-section-card__title')
    certification_titles = [certificate.text.strip() for certificate in certification_titles]

    certification_universities = certificates_list.find_all('a', class_='profile-section-card__subtitle-link')
    certification_universities = [certificate.text.strip() for certificate in certification_universities]

    certification_dates = certificates_list.find_all('div', class_='profile-section-card__meta')
    certification_dates = [certificate.text.strip() for certificate in certification_dates]
    certification_dates = [certificate.split('\n')[0].strip() for certificate in certification_dates if certificate != '']

    merged_certifications = list(zip(certification_titles, certification_universities, certification_dates))
    textified_certifications = [f"{title} from {university} ({date})" for title, university, date in merged_certifications]
    return textified_certifications

def get_educations(soup, source):
    education_list = soup.find("section", class_="core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section education")
    education_titles = education_list.find_all('h3', class_='profile-section-card__title')
    education_titles = [education.text.strip() for education in education_titles]

    education_dates = education_list.find_all('div', class_='profile-section-card__meta')
    education_dates = [education.text.strip() for education in education_dates]
    education_dates = [education.split('\n')[0].strip() for education in education_dates if education != '']

    education_descriptions = education_list.find_all('div', class_='education__item--details')
    education_descriptions = [education.text.strip() for education in education_descriptions]

    merged_educations = list(zip(education_titles, education_dates, education_descriptions))
    textified_educations = [f"{title} ({date}) characterized by the following description: \n{description}" for title, date, description in merged_educations]
    return textified_educations

def get_experiences(soup, source):
    jobs_list = soup.find("section", class_="core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section experience")
    jobs_titles = jobs_list.find_all('h3', class_='profile-section-card__title')
    jobs_titles = [job.text.strip() for job in jobs_titles]

    jobs_companies = jobs_list.find_all('a', class_='profile-section-card__subtitle-link')
    jobs_companies = [job.text.strip() for job in jobs_companies]

    jobs_descriptions = jobs_list.find_all('div', class_='experience-item__description experience-item__meta-item')
    jobs_descriptions = [job.text.strip() for job in jobs_descriptions]

    merged_jobs = list(zip(jobs_titles, jobs_companies, jobs_descriptions))
    textified_jobs = [f"{title} at {company} characterized by the following description: \n{description}" for title, company, description in merged_jobs]
    return textified_jobs

def create_session_with_retries():
    """Create a session with retry strategy and rotating user agents"""
    session = requests.Session()
    
    # Configure retry strategy
    retries = Retry(
        total=5,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504]  # retry on these status codes
    )
    
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    # Rotate between different user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    
    session.headers.update({
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    
    return session

def scrape_job_posting(url):
    """Scrapes the job posting with improved error handling and anti-bot detection"""
    session = create_session_with_retries()
    
    # Add random delay before request
    time.sleep(random.uniform(1, 3))
    
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Wrap element finding in try-except blocks to handle missing elements
        try:
            job_title = soup.find("h1", class_="topcard__title").text.strip()
            company_name = soup.find("a", class_="topcard__org-name-link topcard__flavor--black-link").text.strip()
            company_location = soup.find("span", class_="topcard__flavor topcard__flavor--bullet").text.strip()
            job_description = soup.find("div", class_="description__text description__text--rich").text.strip()
            job_description = job_description.replace("\n", " ")
        except AttributeError:
            job_title, company_name, company_location, job_description = None, None, None, None

        sentences = re.split(r'(?=[A-Z])', job_description)
        salary_keywords = ["$", "€", "£", "¥", "₹", "salary", "salaries"]
        salary_information = ', '.join([sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in salary_keywords)])
        
        return job_posting.JobPosting(job_title, company_name, company_location, job_description, salary_information)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job posting: {e}")
        raise

def query(user_persona, job_posting, prompt):
    llm = ChatOpenAI(temperature=0.5)
    prompt_template = open(prompt, "r").read()
    llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

    marco_inputs = {k: v for k, v in user_persona.__dict__.items()}
    job_inputs = {k: v for k, v in job_posting.__dict__.items()}

    inputs = {**marco_inputs, **job_inputs}
    response = llm_chain(inputs=inputs)

    return response

def main():
    parser = argparse.ArgumentParser(description='Generate a cover letter, resume, and email.')

    parser.add_argument('--prompt', default='src/prompts/cover_letter.txt', help='The prompt to use.')
    parser.add_argument('--profile_url', default=None, help='The URL of the profile to use.')
    parser.add_argument('--job_url', default=None, help='The URL of the job posting to use.')

    args = parser.parse_args()

    # url = input("Enter the URL of the job posting: ")

    # Create UserPersona instance
    source = get_profile_source(args.profile_url)

    user = scrape_profile(source)

    # Create JobPosting instance using scrape_job_posting function
    job = scrape_job_posting(args.job_url)

    # Create Prompt instance
    template = prompt.Template(args.prompt)

    # Generate cover letter
    cover_letter = template.generate_cover_letter(user, job)

    response = query(user, job, template.template)

    print(response)

    input("Press Enter to continue...")

if __name__ == '__main__':
    main()
