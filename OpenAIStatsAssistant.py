
    
from typing import Dict, Any
from pydantic import BaseModel
from enum import Enum
from openai import OpenAI

from dotenv import load_dotenv
import os
from dotenv import load_dotenv
import os

# Load the .env file
current_dir = os.path.dirname(__file__)
env_file_path = os.path.join(current_dir, '.env')
load_dotenv(env_file_path)
# Load the .env file
current_dir = os.path.dirname(__file__)
env_file_path = os.path.join(current_dir, '.env')
load_dotenv(env_file_path)

class Stat(BaseModel):
    STR: int  # Strength
    CON: int  # Constitution
    SIZ: int  # Size
    DEX: int  # Dexterity
    INT: int  # Intelligence
    POW: int  # Power
    CHA: int  # Charisma
    thought_process: str  # New field

class StatLimits(Enum):
    MIN = {"STR": 3, "CON": 3, "DEX": 3, "POW": 3, "CHA": 3, "SIZ": 8, "INT": 8}
    MAX = {"STR": 18, "CON": 18, "DEX": 18, "POW": 18, "CHA": 18, "SIZ": 18, "INT": 18}

class OpenAIStatsAssistant:
    def __init__(self, system_message: str, total_points: int = 80):
        self.system_message = system_message
        self.total_points = total_points
        self.client = OpenAI()
        self.previous_result = None

    def calculate_stats(self, stats: Dict[str, Any]) -> Dict[str, any]:
        result = {
            "stats": {},
            "within_limits": True,
            "points_spent": 0,
            "points_remaining": self.total_points,
            "errors": []
        }

        for stat, value in stats.items():
            if stat not in StatLimits.MIN.value:
                if stat == "thought_process":
                    result["stats"][stat] = value
                else:
                    result["errors"].append(f"Invalid stat: {stat}")
                    result["within_limits"] = False
                continue

            if stat != "thought_process":
                if value < StatLimits.MIN.value[stat] or value > StatLimits.MAX.value[stat]:
                    result["within_limits"] = False
                    result["errors"].append(
                        f"{stat} is out of range ({StatLimits.MIN.value[stat]}-{StatLimits.MAX.value[stat]})")

                result["stats"][stat] = value
                result["points_spent"] += value

        if result["points_spent"] > self.total_points:
            result["within_limits"] = False
            result["errors"].append(
                f"Total points spent ({result['points_spent']}) exceeds the limit of {self.total_points}")

        result["points_remaining"] = max(0, self.total_points - result["points_spent"])

        return result

    def validate_stats(self, stat_object: Stat) -> Dict[str, Any]:
        stats = stat_object.dict()
        result = self.calculate_stats(stats)
        if result['within_limits'] and result['points_remaining'] >= 0 and not result['errors']:
            return {"success": True, "data": result}
        else:
            return {"success": False, "data": result}

    def process_character_creation(self, character_description: str, stats_user_prompt: str) -> Dict[str, Any]:
        attempts = 0
        feedback = ""
        while attempts < 5:
            print(f"Attempt {attempts + 1}: Generating character stats.")
            
            # Combine the original prompts with feedback from previous attempts
            full_prompt = f"{character_description}\n{stats_user_prompt}\n{feedback}"
            
            response = self.generate_character_stats(full_prompt)
            if response is None:
                print("Failed to get a response from the LLM. Retrying...")
                attempts += 1
                continue

            try:
                validation = self.validate_stats(response)
                if validation['success']:
                    print("Successfully generated and validated character stats.")
                    print("Details:", validation['data'])
                    return validation['data']
                else:
                    print("Generated stats did not meet criteria, retrying...")
                    print("Errors:", validation['data']['errors'])
                    
                    # Prepare feedback for the next attempt
                    feedback = f"Previous attempt failed. Please address these issues:\n"
                    for error in validation['data']['errors']:
                        feedback += f"- {error}\n"
                    feedback += "Please try again, keeping in mind the character description and the issues mentioned above."
            except Exception as e:
                print(f"Error during stat validation: {e}")
                feedback = f"An error occurred: {str(e)}. Please try again."

            attempts += 1

        print("Failed to generate valid character stats after 5 attempts.")
        return None
    def generate_character_stats(self, user_prompt: str) -> Any:
        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=Stat
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def generate_stats_from_prompt(self, stats_user_prompt: str) -> Dict[str, Any]:
        """
        Generate character stats based on a custom user prompt.
        """
        response = self.generate_character_stats(stats_user_prompt)
        if response is None:
            return None

        validation = self.validate_stats(response)
        return validation['data'] if validation['success'] else None