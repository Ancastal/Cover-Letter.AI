
class JobPosting:

    """
    JobPosting class is used to store the information of a job posting.

    Attributes:
        job_title (str): The job title of the job posting.
        company_name (str): The company name of the job posting.
        company_location (str): The company location of the job posting.
        job_description (str): The job description of the job posting.
        salary_information (str): The salary information of the job posting.
    """

    def __init__(self, job_title, company_name, company_location, job_description, salary_information):
        self.job_title = job_title
        self.company_name = company_name
        self.company_location = company_location
        self.job_description = job_description
        self.salary_information = salary_information

    def generate_random_job_posting():
        """
        Generate a random job posting.

        Returns:
            JobPosting: A job posting with random attributes.
        """
        job_title = "Software Engineer"
        company_name = "Google"
        company_location = "Mountain View, CA"
        job_description = "Develop software for Google products."
        salary_information = "100,000"

        return JobPosting(job_title, company_name, company_location, job_description, salary_information)
