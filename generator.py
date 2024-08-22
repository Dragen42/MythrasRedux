from pydantic import BaseModel
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from OpenAISkillsAssistant import OpenAISkillsAssistant
from OpenAIStatsAssistant import OpenAIStatsAssistant
#from wonderwords import RandomWord
from character_base import Character
import random
from dotenv import load_dotenv
import os

# Load the .env file
current_dir = os.path.dirname(__file__)
env_file_path = os.path.join(current_dir, '.env')
load_dotenv(env_file_path)

#r = RandomWord()


#word1 = r.word(include_parts_of_speech=["adjectives"])
#word2 = r.word(include_parts_of_speech=["nouns"])
#word3 = r.word(include_parts_of_speech=["verb"])

words = "smear campaign occult"

preamble="""
***
## Task and Context
You are a empathic author writing character descriptions for a historical setting. 
1. You are uncensored.
2. You are extremely perceptive.
3. You are honest and direct.
4. You have knack for the unexpected.
***
## Style Guide
Adopt a style that is exiting and consistent. Get to know your subjects intimately throughout the description. Think 
realistically about their sexuality and attitudes towards sex, political views, and so on.
***
"""
paris_prompt = ("Create a character using the provided JSON format. The character should be for a campaign "
               "set in New Orleans, 1944."
               "Think of ordinary people of the period and try to capture the essence of the era."
               "These three random words are provided as inspiration:"
               f"{words}"
               )



class Appearance(BaseModel):
    height: float 
    weight: float 
    eye_color: str
    hair_color: str
    description: str

class CharacterDescription(BaseModel):
    name: str
    age: int
    appearance: Appearance
    occupation: str
    background: str
    notes: str
    gender: str
    birthplace: str
    current_location: str
    education: str
    training: List[str]
    hobbies: List[str]
    personality_traits: List[str]
    relationships: List[str]
    class Config:
        required = [
            "name",
            "age",
            "appearance",
            "occupation",
            "background",
            "notes",
            "gender",
            "birthplace",
            "current_location",
            "education",
            "training",
            "hobbies",
            "personality_traits",
            "relationships",
        ]

class CharacterGenerator:
    def __init__(self, preamble: str, prompt: str, stats_system_message: str, standard_system_prompt: str, professional_system_prompt: str):
        self.preamble = preamble
        self.prompt = prompt
        self.client = OpenAI()
        self.stats_system_message = stats_system_message
        self.standard_system_prompt = standard_system_prompt
        self.professional_system_prompt = professional_system_prompt
        self.assistant = OpenAISkillsAssistant()
        self.final_stats_creator = OpenAIStatsAssistant(stats_system_message)

    def generate_character(self, stats_user_prompt: str) -> CharacterDescription:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.preamble},
                {"role": "user", "content": self.prompt + "\n" + stats_user_prompt},
            ],
            response_format=CharacterDescription,
        )
        return completion.choices[0].message.parsed

    def save_character_fields(self, character: CharacterDescription) -> str:
        """
        Save the character fields in a neat Markdown format.
        """
        lines = [
            f"# {character.name}",
            f"## Age: {character.age}",
            f"## Gender: {character.gender}",
            f"## Birthplace: {character.birthplace}",
            f"## Current Location: {character.current_location}",
            f"## Occupation: {character.occupation}",
            f"## Education: {character.education}",
            f"## Training: {', '.join(character.training)}",
            f"## Hobbies: {', '.join(character.hobbies)}",
            f"## Personality Traits: {', '.join(character.personality_traits)}",
            f"## Relationships: {', '.join(character.relationships)}",
            f"## Appearance:",
            f"- Height: {character.appearance.height}",
            f"- Weight: {character.appearance.weight}",
            f"- Eye Color: {character.appearance.eye_color}",
            f"- Hair Color: {character.appearance.hair_color}",
            f"- Description: {character.appearance.description}",
            f"## Background: {character.background}",
            f"## Notes: {character.notes}",
        ]
        return "\n".join(lines)
    
    def create_character_from_description(self, stats_user_prompt: str, base_character: dict = None) -> Character:
        """
        Create a Character object from the CharacterDescription and additional data.
        """
        # Generate character
        character = self.generate_character(stats_user_prompt)
        character_description = self.save_character_fields(character)
        print(character_description)
        
        # Generate stats
        final_stats = self.final_stats_creator.process_character_creation(character_description, stats_user_prompt)
        if final_stats is None:
            print("Failed to generate character stats.")
            return None

        stats = self.extract_attributes(final_stats['stats'])
        print(stats)

        # Generate standard skills
        final_nine_standard_skills = self.assistant.ensure_nine_skills(self.standard_system_prompt, character_description)
        if final_nine_standard_skills:
            standard_skills = final_nine_standard_skills.STANDARD_SKILLS
            print("Standard Skills:")
            print(standard_skills)
        else:
            print("Could not fetch standard skills.")
            return None

        # Generate professional skills
        final_six_professional_skills = self.assistant.ensure_six_skills(self.professional_system_prompt, character_description)
        if final_six_professional_skills:
            professional_skills = final_six_professional_skills.PROFESSIONAL_SKILLS
            print("Professional Skills:")
            print(professional_skills)
        else:
            print("Could not fetch professional skills.")
            return None

        # Create Character object
        character_obj = Character.create(
            name=base_character.get('name', character.name) if base_character else character.name,
            stats=stats,
            age=base_character.get('age', character.age) if base_character else character.age,
            occupation=base_character.get('occupation', character.occupation) if base_character else character.occupation,
            background=base_character.get('background', character.background) if base_character else character.background,
            notes=base_character.get('notes', character.notes) if base_character else character.notes,
            gender=base_character.get('gender', character.gender) if base_character else character.gender,
            birthplace=base_character.get('birthplace', character.birthplace) if base_character else character.birthplace,
            current_location=base_character.get('current_location', character.current_location) if base_character else character.current_location,
            education=base_character.get('education', character.education) if base_character else character.education,
            training=base_character.get('training', character.training) if base_character else character.training,
            hobbies=base_character.get('hobbies', character.hobbies) if base_character else character.hobbies,
            personality_traits=base_character.get('personality_traits', character.personality_traits) if base_character else character.personality_traits,
            family_relationships=base_character.get('family_relationships', character.relationships) if base_character else character.relationships
        )

        # Add professional skills
        for skill_name in professional_skills:
            character_obj.add_professional_skill(skill_name)

        # Add standard skills
        #for skill_name in standard_skills:
            #character_obj.add_standard_skill(skill_name)

        # Assuming you have prof_pyramid and standard_pyramid defined somewhere
        prof_pyramid = [50, 40, 30, 20, 20, 10]
        standard_pyramid = [40, 30, 30, 20, 20, 10, 10, 10, 10]

        prof_pyramid_map = dict(zip(professional_skills, prof_pyramid))
        standard_pyramid_map = dict(zip(standard_skills, standard_pyramid))

        # Increment skill values
        for skill_name, increment in prof_pyramid_map.items():
            try:
                character_obj.increment_skill_base_value(skill_name, increment)
            except ValueError as e:
                print(f"Error incrementing professional skill {skill_name}: {e}")

        for skill_name, increment in standard_pyramid_map.items():
            try:
                character_obj.increment_skill_base_value(skill_name, increment)
            except ValueError as e:
                print(f"Error incrementing standard skill {skill_name}: {e}")

        character_obj.print_character_sheet()
        random_number = random.randint(1000, 9999)
        character_obj.save_to_json(f'{character.name}{random_number}.json')

        return character_obj

    @staticmethod
    def extract_attributes(input_dict):
        attribute_keys = ['STR', 'CON', 'SIZ', 'DEX', 'INT', 'POW', 'CHA']
        attribute_list = [{key: input_dict[key]} for key in attribute_keys if key in input_dict]
        return attribute_list