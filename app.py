"""An application to generate cover letters based on user information and job postings."""
import streamlit as st
from src.cover_letter import scrape_job_posting, query, user_persona
import subprocess
import sys
import os
import time


try:
    from linkedin_api import Linkedin
except ModuleNotFoundError as e:
    subprocess.Popen([f'{sys.executable} -m pip install git+https://github.com/tomquirk/linkedin-api.git'], shell=True)
  # wait for subprocess to install package before running your actual code below
    time.sleep(90)


st.set_page_config(page_title='Cover Letter Generator', page_icon=':page_with_curl:')

def scrape_profile(profile_id):
    email = os.getenv('LINKEDIN_EMAIL')
    pwd = os.getenv('LINKEDIN_PASSWORD')
    api = Linkedin(email, pwd)
    profile = api.get_profile(profile_id)

    name = profile['firstName'] + ' ' + profile['lastName']
    education = [f"{education['schoolName']} ({education['timePeriod']['startDate']['year']}) characterized by the following description: \
                 \n{education['description']}" for education in profile['education']]
    experience = profile['experience']
    experience = [f"{experience['title']} at {experience['companyName']} characterized by the following description:  \
                  \n{experience['description']}" for experience in profile['experience']]
    certifications = profile['certifications']
    certifications = [f"{certification['name']} from {certification['authority']}" for certification in profile['certifications']]
    skills = api.get_profile_skills(profile_id)
    skills = [skill['name'] for skill in skills]
    return user_persona.UserPersona(name, education, experience, skills, certifications)

# Function to display the app
def main():
    # App title

    st.title('Cover Letter Generator :page_with_curl:')
    st.write('This app generates a cover letter based on your information and a job posting.')
    st.caption('Currently, this app only supports LinkedIn job postings, e.g. https://www.linkedin.com/jobs/view/3544765357/')
    st.caption('User profile parsing is not available in this Cloud version of the app. Please, use the local version instead.')
    st.write('---')


    # Job Posting URL input
    st.subheader(':clipboard: Enter LinkedIn Job Posting URL')
    url = st.text_input('Job URL', '')
    st.subheader(':clipboard: Enter LinkedIn Profile URL')
    user_profile = st.text_input('Profile URL', '')
    customize_profile = st.checkbox('Customize your Profile')
    if customize_profile:
                # User Inputs Section
        st.subheader(':bust_in_silhouette: Enter your details')
        name = st.text_input('Name', 'John Doe')
        columns = st.columns(2)
        with columns[0]:
            education_level = st.selectbox('Education Level', ['High School', 'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD'])
        with columns[1]:
            fields = [
                'Accounting', 'Agriculture', 'Anthropology', 'Architecture', 'Art', 'Biology', 'Business', 'Chemistry',
                'Communications', 'Computer Science', 'Criminal Justice', 'Culinary Arts', 'Dentistry',
                'Economics', 'Education', 'Engineering', 'Finance', 'Geography', 'History', 'Journalism',
                'Law', 'Linguistics', 'Marketing', 'Mathematics', 'Medicine', 'Music', 'Nursing',
                'Pharmacy', 'Philosophy', 'Physics', 'Political Science', 'Psychology', 'Religion',
                'Social Work', 'Sociology', 'Theatre', 'Veterinary Medicine', 'Other'
            ]
        education_field = st.selectbox('Field of Study', fields)
        education = f"{education_level} in {education_field}"
        experience = st.text_area('Please, describe your work experience', '5 years of experience in software engineering at Google')
        skills = st.multiselect('Skills', ['Python', 'SQL', 'Java', 'JavaScript', 'C#', 'C++', 'PHP', 'Swift', 'Rust'])
        certifications = st.multiselect('Certifications', ['AWS', 'Google Cloud', 'Azure', 'Cisco', 'CompTIA', 'PMP',
                                                            'Project+', 'CAPM', 'Security+', 'Network+', 'A+', 'CISSP',
                                                        ])
        st.write('---')

    # Generate Cover Letter
    if st.button('Generate Cover Letter'):
        container = st.empty()
        container.success("Please, wait while we generate your cover letter...")  # Display success alert


        if customize_profile:
            user = user_persona.UserPersona(name, education, experience, skills, certifications)
        else:
            api = Linkedin('ancastal@outlook.it', 'Respublica96.')
            profile_id = user_profile.split('/')[-2]
            user = scrape_profile(profile_id)

        job_posting = scrape_job_posting(url)

        # Call the imported function
        response = query(user, job_posting, 'src/prompts/cover_letter.txt')

        container.empty()  # Clear the success alert

        # Display result
        st.subheader('Generated Cover Letter :memo:')
        st.write(response['text'])

if __name__ == '__main__':
    main()
