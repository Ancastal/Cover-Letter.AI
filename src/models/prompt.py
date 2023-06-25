
class Template:
    def __init__(self, template):
        self.template = template

    def generate_cover_letter(self, user_persona, job_posting):
        """
        Generate a cover letter using the user's persona and the job posting.

        Parameters
        ----------
        user_persona : UserPersona
            The user's persona.
        job_posting : JobPosting
            The job posting.

        Returns
        -------
        cover_letter : str
            The generated cover letter.
        """

        cover_letter = self.template.format(
            job_title=job_posting.job_title,
            company_name=job_posting.company_name,
            company_location=job_posting.company_location,
            job_description=job_posting.job_description,
            salary_information=job_posting.salary_information,
            name=user_persona.name,
            education=user_persona.education,
            experience=user_persona.experience,
            skills=user_persona.skills,
            certifications=user_persona.certifications
        )
        return cover_letter

    def generate_resume(self, user_persona):
        resume = self.template.format(
            name=user_persona.name,
            education=user_persona.education,
            experience=user_persona.experience,
            skills=user_persona.skills,
            certifications=user_persona.certifications
        )
        return resume

    def generate_email(self, user_persona, job_posting):
        email = self.template.format(
            job_title=job_posting.job_title,
            company_name=job_posting.company_name,
            company_location=job_posting.company_location,
            job_description=job_posting.job_description,
            salary_information=job_posting.salary_information,
            name=user_persona.name,
            education=user_persona.education,
            experience=user_persona.experience,
            skills=user_persona.skills,
            certifications=user_persona.certifications
        )
        return email
