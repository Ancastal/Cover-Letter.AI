
class UserPersona:

    """
    UserPersona class is a class that represents a user persona.

    Attributes:
        name (str): The name of the user persona.
        education (str): The education of the user persona.
        experience (str): The experience of the user persona.
        skills (str): The skills of the user persona.
        certifications (str): The certifications of the user persona.
    """

    def __init__(self, name, education, experience, skills, certifications):
        self.name = name
        self.education = education
        self.experience = experience
        self.skills = skills
        self.certifications = certifications

    def generate_random_user_persona():
        """
        Generate a random user persona.

        Returns:
            UserPersona: A user persona with random attributes.
        """
        name = "John Doe"
        education = "Bachelor's Degree"
        experience = "5 years of experience"
        skills = "Python, SQL, Java"
        certifications = "AWS, Google Cloud"

        return UserPersona(name, education, experience, skills, certifications)
