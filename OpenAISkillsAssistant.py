from typing import Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file
current_dir = os.path.dirname(__file__)
env_file_path = os.path.join(current_dir, '.env')
load_dotenv(env_file_path)




class SkillsStandard(BaseModel):
    STANDARD_SKILLS: list[str]
    thought_process: str

class SkillsProfessional(BaseModel):
    PROFESSIONAL_SKILLS: list[str]
    thought_process: str

class OpenAISkillsAssistant:
    def __init__(self):
        self.client = OpenAI()

    def ensure_nine_skills(self, standard_system_prompt: str, character_description: str, max_attempts: int = 5) -> SkillsStandard:
        """
        Ensure the fetched skills list contains exactly nine skills, retrying if necessary.

        Args:
            standard_system_prompt (str): System prompt for the LLM.
            character_description (str): User prompt for the LLM.
            max_attempts (int): Maximum number of attempts to fetch the skills.

        Returns:
            SkillsStandard or None: Returns the skills model if successful, None if not.
        """
        attempts = 0
        while attempts < max_attempts:
            print(f"Attempt {attempts + 1}: Fetching skills.")
            skills_standard = self.fetch_skills(standard_system_prompt, character_description, SkillsStandard)
            if skills_standard and len(skills_standard.STANDARD_SKILLS) == 9:
                print("Successfully retrieved exactly nine skills.")
                return skills_standard
            else:
                if skills_standard:
                    print(f"Retrieved {len(skills_standard.STANDARD_SKILLS)} skills, but 9 are required. Retrying...")
                else:
                    print("Failed to retrieve skills. Retrying...")
            attempts += 1

        print("Failed to retrieve exactly nine skills after maximum attempts.")
        return None

    def ensure_six_skills(self, professional_system_prompt: str, character_description: str, max_attempts: int = 5) -> SkillsProfessional:
        """
        Ensure the fetched skills list contains exactly six skills, retrying if necessary.

        Args:
            professional_system_prompt (str): System prompt for the LLM.
            character_description (str): User prompt for the LLM.
            max_attempts (int): Maximum number of attempts to fetch the skills.

        Returns:
            SkillsProfessional or None: Returns the skills model if successful, None if not.
        """
        attempts = 0
        while attempts < max_attempts:
            print(f"Attempt {attempts + 1}: Fetching skills.")
            skills_professional = self.fetch_skills(professional_system_prompt, character_description, SkillsProfessional)
            if skills_professional and len(skills_professional.PROFESSIONAL_SKILLS) == 6:
                print("Successfully retrieved exactly six skills.")
                return skills_professional
            else:
                if skills_professional:
                    print(f"Retrieved {len(skills_professional.PROFESSIONAL_SKILLS)} skills, but 6 are required. Retrying...")
                else:
                    print("Failed to retrieve skills. Retrying...")
            attempts += 1

        print("Failed to retrieve exactly six skills after maximum attempts.")
        return None

    def fetch_skills(self, system_prompt: str, standard_prompt: str, response_format: type) -> BaseModel:
        """
        Fetch skills from the OpenAI model using provided prompts and return a structured response.

        Args:
            system_prompt (str): The system-defined prompt setting the context for the LLM.
            standard_prompt (str): The user prompt asking for specific information.
            response_format (type): The desired response format (SkillsStandard or SkillsProfessional).

        Returns:
            BaseModel: A pydantic model containing the structured response.
        """
        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": standard_prompt}
                ],
                response_format=response_format,
            )

            # Access the first choice's parsed message as a structured object
            skills_data = completion.choices[0].message.parsed
            return skills_data

        except Exception as e:
            print(f"An error occurred: {e}")
            return None