from typing import List, Optional, Dict, ClassVar, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
from textwrap import dedent
import json
from pathlib import Path
from dataclasses import dataclass


class StatLimits(Enum):
    MIN = {"STR": 3, "CON": 3, "DEX": 3, "POW": 3, "CHA": 3, "SIZ": 8, "INT": 8}
    MAX = {"STR": 18, "CON": 18, "DEX": 18, "POW": 18, "CHA": 18, "SIZ": 18, "INT": 18}


def stat_field(stat_name: str) -> Field:
    return Field(None, ge=StatLimits.MIN.value[stat_name], le=StatLimits.MAX.value[stat_name])


class Stat(BaseModel):
    STR: Optional[int] = stat_field("STR")
    CON: Optional[int] = stat_field("CON")
    SIZ: Optional[int] = stat_field("SIZ")
    DEX: Optional[int] = stat_field("DEX")
    INT: Optional[int] = stat_field("INT")
    POW: Optional[int] = stat_field("POW")
    CHA: Optional[int] = stat_field("CHA")


@dataclass
class Skill:
    name: str
    value: int
    base_value: int


@dataclass
class HitLocation:
    name: str
    range: str
    hp: int
    ap: int


@dataclass
class CombatStyle:
    weapons: List[str]
    name: str
    value: int


class SkillCategory(Enum):
    STANDARD = "standard"
    PROFESSIONAL = "professional"


@dataclass
class Attributes:
    action_points: int = 3
    damage_modifier: str = ""
    magic_points: int = 0
    strike_rank: str = ""
    movement: str = "6"


def default_human_hit_locations() -> List[HitLocation]:
    return [
        HitLocation(name="Right leg", range="01-03", hp=5, ap=0),
        HitLocation(name="Left leg", range="04-06", hp=5, ap=0),
        HitLocation(name="Abdomen", range="07-09", hp=6, ap=0),
        HitLocation(name="Chest", range="10-12", hp=7, ap=0),
        HitLocation(name="Right arm", range="13-15", hp=4, ap=0),
        HitLocation(name="Left arm", range="16-18", hp=4, ap=0),
        HitLocation(name="Head", range="19-20", hp=5, ap=0)
    ]





class Character(BaseModel):
    name: str
    gender: Optional[str] = None
    age: int
    height: Optional[float] = None
    weight: Optional[float] = None
    eye_color: Optional[str] = None
    hair_color: Optional[str] = None
    appearance: Optional[str] = None
    cult_rank: str
    occupation: str
    background: str
    birthplace: Optional[str] = None
    current_location: Optional[str] = None
    education: Optional[str] = None
    training: Optional[List[str]] = None
    hobbies: Optional[List[str]] = None
    personality_traits: Optional[List[str]] = None
    family_relationships: Union[Dict[str, Any], List[str]]
    stats: List[Dict[str, int]] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    folk_spells: List[str] = Field(default_factory=list)
    theism_spells: List[str] = Field(default_factory=list)
    sorcery_spells: List[str] = Field(default_factory=list)
    mysticism_spells: List[str] = Field(default_factory=list)
    hit_locations: List[HitLocation]
    combat_styles: List[CombatStyle] = Field(default_factory=list)
    attributes: Attributes = Field(default_factory=Attributes)
    notes: str = ""
    features: List[str] = Field(default_factory=list)
    cults: List[str] = Field(default_factory=list)
    spirits: List[str] = Field(default_factory=list)
    natural_armor: bool = False
    
    @validator('family_relationships', pre=True)
    def convert_to_dict(cls, v):
        if isinstance(v, list):
            return {f'Relationship {i+1}': r for i, r in enumerate(v)}
        return v

    @classmethod
    def create(cls,
               name: str,
               stats: List[Dict[str, int]],
               age: int,
               height: Optional[float] = None,
               weight: Optional[float] = None,
               eye_color: Optional[str] = None,
               hair_color: Optional[str] = None,
               appearance: Optional[str] = None,
               gender: Optional[str] = None,
               occupation: Optional[str] = None,
               background: Optional[str] = None,
               birthplace: Optional[str] = None,
               current_location: Optional[str] = None,
               education: Optional[str] = None,
               training: Optional[List[str]] = None,
               hobbies: Optional[List[str]] = None,
               personality_traits: Optional[List[str]] = None,
               family_relationships: Any = None,
               skills: Optional[List[Skill]] = None,
               cult_rank: str = "",
               notes: str = "",
               features: Optional[List[str]] = None,
               cults: Optional[List[str]] = None,
               spirits: Optional[List[str]] = None,
               natural_armor: bool = False,
               additional_skills: Optional[List[Dict[str, SkillCategory]]] = None) -> 'Character':
        """
        Factory method to create a new character with initialized attributes and skills.

        :param name: Character name
        :param cult_rank: Character's cult rank
        :param stats: List of dictionaries containing character stats
        :param notes: Additional notes about the character
        :param features: List of character features
        :param cults: List of cults the character belongs to
        :param spirits: List of spirits associated with the character
        :param natural_armor: Whether the character has natural armor
        :param additional_skills: List of additional skills to add, each as a dict with skill name and category
        :return: Initialized Character instance
        """


        character = cls(
            name=name,
            gender=gender or "",
            age=age,
            height=height or 0,
            weight=weight or 0,
            eye_color=eye_color or "",
            hair_color=hair_color or "",
            occupation=occupation or "",
            background=background or "",
            birthplace=birthplace or "",
            current_location=current_location or "",
            education=education or "",
            training=training or [],
            hobbies=hobbies or [],
            personality_traits=personality_traits or [],
            family_relationships=family_relationships or {},
            skills=skills or [],
            combat_styles=[],
            appearance=appearance or "",
            cult_rank=cult_rank or "",
            stats=stats,
            hit_locations=default_human_hit_locations(),
            notes=notes,
            features=features or [],
            cults=cults or [],
            spirits=spirits or [],
            natural_armor=natural_armor
        )

        # Initialize standard skills
        character.initialize_standard_skills()

        # Add additional skills if provided
        if additional_skills:
            for skill_info in additional_skills:
                for skill_name, category in skill_info.items():
                    if category == SkillCategory.STANDARD:
                        character.add_standard_skill(skill_name)
                    elif category == SkillCategory.PROFESSIONAL:
                        character.add_professional_skill(skill_name)

        # Calculate initial attributes and skill values
        character.calculate_skill_values_based_on_stats()

        return character

    def calculate_hit_points(self) -> None:
        """
        Calculate and assign hit points to each location on the character's body.

        This function calculates the hit points for each location on the character's body based on their Constitution (CON) and Size (SIZ) stats. The hit points are assigned to each location's `hp` attribute.

        Parameters:
            self (Character): The character object.

        Returns:
            None
        """
        CON = next(stat["CON"] for stat in self.stats if "CON" in stat)
        SIZ = next(stat["SIZ"] for stat in self.stats if "SIZ" in stat)
        CON_SIZ = CON + SIZ
        hit_points = {
            "Head": (CON_SIZ - 1) // 5 + 1,
            "Chest": (CON_SIZ - 1) // 5 + 3,
            "Abdomen": (CON_SIZ - 1) // 5 + 2,
            "Each Arm": (CON_SIZ - 1) // 5 + 1 if CON_SIZ <= 10 else (CON_SIZ - 6) // 5 + 2,
            "Each Leg": (CON_SIZ - 1) // 5 + 1
        }
        for location in self.hit_locations:
            if location.name in ["Right arm", "Left arm"]:
                location.hp = hit_points["Each Arm"]
            elif location.name in ["Right leg", "Left leg"]:
                location.hp = hit_points["Each Leg"]
            else:
                location.hp = hit_points[location.name]

    @property
    def hit_points(self) -> Dict[str, int]:
        """Calculate and return hit points for all locations."""
        self.calculate_hit_points()
        return {loc.name: loc.hp for loc in self.hit_locations}

    def calculate_damage_modifier(self) -> None:
        """
        Calculate the damage modifier based on the character's Strength (STR) and Size (SIZ) stats.

        The damage modifier is determined by the sum of the Strength and Size stats.
        The range of damage modifiers is as follows:
        - STR_SIZ <= 5: -1d8
        - 6 <= STR_SIZ <= 10: -1d6
        - 11 <= STR_SIZ <= 15: -1d4
        - 16 <= STR_SIZ <= 20: -1d2
        - 21 <= STR_SIZ <= 25: +0
        - 26 <= STR_SIZ <= 30: +1d2
        - 31 <= STR_SIZ <= 35: +1d4
        - 36 <= STR_SIZ <= 40: +1d6
        - 41 <= STR_SIZ <= 45: +1d8
        - 46 <= STR_SIZ <= 50: +1d10
        - 51 <= STR_SIZ <= 60: +1d12
        - STR_SIZ > 60: +2d6

        The calculated damage modifier is assigned to the `damage_modifier` attribute of the `attributes` object.
        This function does not return any value.
        """
        STR = next(stat["STR"] for stat in self.stats if "STR" in stat)
        SIZ = next(stat["SIZ"] for stat in self.stats if "SIZ" in stat)
        STR_SIZ = STR + SIZ
        if STR_SIZ <= 5:
            damage_modifier = "-1d8"
        elif STR_SIZ <= 10:
            damage_modifier = "-1d6"
        elif STR_SIZ <= 15:
            damage_modifier = "-1d4"
        elif STR_SIZ <= 20:
            damage_modifier = "-1d2"
        elif STR_SIZ <= 25:
            damage_modifier = "+0"
        elif STR_SIZ <= 30:
            damage_modifier = "+1d2"
        elif STR_SIZ <= 35:
            damage_modifier = "+1d4"
        elif STR_SIZ <= 40:
            damage_modifier = "+1d6"
        elif STR_SIZ <= 45:
            damage_modifier = "+1d8"
        elif STR_SIZ <= 50:
            damage_modifier = "+1d10"
        else:
            damage_modifier = "+1d12" if STR_SIZ <= 60 else "+2d6"

        self.attributes.damage_modifier = damage_modifier

    @property
    def damage_modifier(self) -> str:
        """Calculate and return the damage modifier."""
        self.calculate_damage_modifier()
        return self.attributes.damage_modifier

    def calculate_magic_points(self) -> None:
        """Calculate the magic points of the character."""
        POW = next(stat["POW"] for stat in self.stats if "POW" in stat)
        self.attributes.magic_points = POW

    @property
    def magic_points(self) -> int:
        """Calculate and return magic points."""
        self.calculate_magic_points()
        return self.attributes.magic_points

    def calculate_strike_rank(self) -> None:
        """
        Calculate the strike rank based on the DEX and INT attributes of the character.
        The strike rank is calculated by summing the DEX and INT attributes and dividing the result by 2.
        The calculated strike rank is then assigned to the 'strike_rank' attribute of the 'attributes' object.
        Parameters:
            None
        Returns:
            None
        """
        DEX = next(stat["DEX"] for stat in self.stats if "DEX" in stat)
        INT = next(stat["INT"] for stat in self.stats if "INT" in stat)
        DEX_INT = DEX + INT
        self.attributes.strike_rank = f"{DEX_INT // 2}"

    @property
    def strike_rank(self) -> str:
        """Calculate and return strike rank."""
        self.calculate_strike_rank()
        return self.attributes.strike_rank

    PROFESSIONAL_SKILLS: ClassVar[Dict[str, List[str]]] = {
        "acting": ["CHA", "CHA"],
        "acrobatics": ["STR", "DEX"],
        "art": ["POW", "CHA"],
        "bureaucracy": ["INT", "CHA"],
        "combat_style": ["STR", "DEX"],
        "commerce": ["POW", "CHA"],
        "comms": ["INT", "CHA"],
        "computers": ["INT", "INT"],
        "courtesy": ["INT", "CHA"],
        "craft": ["DEX", "INT"],
        "culture": ["INT", "INT"],
        "demolitions": ["INT", "POW"],
        "disguise": ["INT", "CHA"],
        "electronics": ["DEX", "INT"],
        "engineering": ["INT", "INT"],
        "forgery": ["DEX", "INT"],
        "gambling": ["INT", "POW"],
        "knowledge": ["INT", "INT"],
        "lockpicking": ["DEX", "DEX"],
        "mechanics": ["DEX", "INT"],
        "medicine": ["INT", "POW"],
        "musicianship": ["DEX", "CHA"],
        "navigation": ["INT", "POW"],
        "oratory": ["POW", "CHA"],
        "pilot": ["DEX", "INT"],
        "politics": ["INT", "CHA"],
        "research": ["INT", "POW"],
        "science": ["INT", "INT"],
        "seamanship": ["INT", "CON"],
        "seduction": ["INT", "CHA"],
        "sensors": ["INT", "POW"],
        "sleight": ["DEX", "CHA"],
        "streetwise": ["POW", "CHA"],
        "survival": ["CON", "POW"],
        "teaching": ["INT", "CHA"],
        "track": ["INT", "CON"]
    }

    STANDARD_SKILLS: ClassVar[Dict[str, List[str]]] = {
        "athletics": ["STR", "DEX"],
        "boating": ["STR", "CON"],
        "brawn": ["STR", "SIZ"],
        "conceal": ["DEX", "POW"],
        "customs": ["INT", "INT"],
        "dance": ["DEX", "CHA"],
        "deceit": ["INT", "CHA"],
        "drive": ["DEX", "POW"],
        "endurance": ["CON", "CON"],
        "evade": ["DEX", "DEX"],
        "first aid": ["DEX", "INT"],
        "influence": ["CHA", "CHA"],
        "insight": ["INT", "POW"],
        "locale": ["INT", "INT"],
        "native tongue": ["INT", "CHA"],
        "perception": ["INT", "POW"],
        "ride": ["DEX", "POW"],
        "sing": ["POW", "CHA"],
        "stealth": ["DEX", "INT"],
        "swim": ["STR", "CON"],
        "willpower": ["POW", "POW"]
    }

    def model_post_init(self, __context: Any) -> None:
        """
        Initializes the standard skills for the character.
        This function iterates over the `STANDARD_SKILLS` dictionary and for each skill, it calculates the base value
        by calling the `calculate_base_value` method with the corresponding attributes. Then, it creates a new `Skill`
        object with the skill name, calculated base value, and base value, and appends it to the `skills` list.
        Parameters:
            self (Character): The character instance.
        Returns:
            None
        """
        pass

    def initialize_standard_skills(self):
        for skill_name, attributes in self.STANDARD_SKILLS.items():
            base_value = self.calculate_base_value(attributes)
            self.skills.append(Skill(name=skill_name, value=base_value, base_value=base_value))

    def add_skill(self, skill_name: str, category: SkillCategory) -> None:
        """
        Adds a skill to the character's skill list based on the provided skill name and category.

        Args:
            skill_name (str): The name of the skill to add.
            category (SkillCategory): The category of the skill (PROFESSIONAL or STANDARD).

        Returns:
            None: This function does not return anything.

        Raises:
            None: This function does not raise any exceptions.

        Description:
            This function checks if the provided skill name exists in the corresponding skill dictionary
            (PROFESSIONAL_SKILLS or STANDARD_SKILLS) based on the provided category. If the skill name is
            found, it retrieves the corresponding attributes and calculates the base value of the skill using
            the `calculate_base_value` method. The calculated base value is then assigned to both the `base_value`
            and `value` attributes of a new `Skill` object, which is appended to the character's `skills` list.

            If the skill name is not found in the corresponding skill dictionary, a warning message is printed
            indicating that the skill was not found in the specified category.

        """
        skill_dict = self.PROFESSIONAL_SKILLS if category == SkillCategory.PROFESSIONAL else self.STANDARD_SKILLS
        if skill_name in skill_dict:
            attributes = skill_dict[skill_name]
            base_value = self.calculate_base_value(attributes)
            self.skills.append(Skill(name=skill_name, value=base_value, base_value=base_value))
        else:
            print(f"Warning: Skill '{skill_name}' not found in {category.value} skills. Skipping.")

    def add_standard_skill(self, skill_name: str) -> None:
        """
        Add a standard skill to the character.

        Args:
            skill_name (str): The name of the skill to add.

        Returns:
            None: This function does not return anything.

        Description:
            This function adds a standard skill to the character by calling the `add_skill` method with the
            provided `skill_name` and `SkillCategory.STANDARD` as arguments. The `add_skill` method is responsible
            for adding the skill to the character's skill list based on the provided skill name and category.
        """
        self.add_skill(skill_name, SkillCategory.STANDARD)

    def add_professional_skill(self, skill_name: str) -> None:
        """
        Add a professional skill to the character.

        Args:
            skill_name (str): The name of the skill to add.

        Returns:
            None: This function does not return anything.

        Raises:
            None: This function does not raise any exceptions.

        Description:
            This function adds a professional skill to the character by calling the `add_skill` method with the
            provided `skill_name` and `SkillCategory.PROFESSIONAL` as arguments. The `add_skill` method is responsible
            for adding the skill to the character's skill list based on the provided skill name and category.
        """
        self.add_skill(skill_name, SkillCategory.PROFESSIONAL)

    def calculate_base_value(self, attributes: List[str]) -> int:
        """
        Calculate the base value of a character based on a list of attributes.

        Args:
            attributes (List[str]): A list of attribute names.

        Returns:
            int: The sum of the values of the attributes in the character's stats.
        """
        return sum(next(stat[attr] for stat in self.stats if attr in stat) for attr in attributes)

    def calculate_skill_values_based_on_stats(self):
        """
        Calculates the skill values based on the corresponding stats for each skill in the character's skills list.

        This function iterates over each skill in the `skills` list and checks if the skill name is present in either
        the `STANDARD_SKILLS` or `PROFESSIONAL_SKILLS` dictionaries. If the skill name is found, it retrieves the
        corresponding attributes and calculates the base value of the skill using the `calculate_base_value` method.
        The calculated base value is then assigned to both the `base_value` and `value` attributes of the skill.

        Parameters:
            self (Character): The character instance.

        Returns:
            None
        """
        for skill in self.skills:
            if skill.name in self.STANDARD_SKILLS:
                attributes = self.STANDARD_SKILLS[skill.name]
            elif skill.name in self.PROFESSIONAL_SKILLS:
                attributes = self.PROFESSIONAL_SKILLS[skill.name]
            else:
                continue

            skill.base_value = self.calculate_base_value(attributes)
            skill.value = skill.base_value  # You may want to add any additional modifiers here

    def increment_skill_base_value(self, skill_name: str, increment: int) -> None:
        """
        Increment the base value of a specified skill.

        Args:
            skill_name (str): The name of the skill to be incremented.
            increment (int): The amount to add to the skill's base value.

        Returns:
            None

        Raises:
            ValueError: If the specified skill is not found in the character's skills list.
        """
        # Find the skill object with the matching name
        skill = next((s for s in self.skills if s.name == skill_name), None)

        # Check if the skill was found
        if skill is not None:
            skill.value += increment
            print(f"Skill '{skill_name}' base value incremented by {increment}. New base value: {skill.base_value}")
        else:
            # If the skill does not exist, raise an error
            raise ValueError(f"No skill found with the name '{skill_name}'")

    def save_to_json(self, file_path: str) -> None:
        """
        Save the character data to a JSON file.

        :param file_path: The path where the JSON file will be saved
        """
        character_dict = self.dict()

        # Convert skills to the desired format
        character_dict['skills'] = [
            {skill.name: skill.value}
            for skill in self.skills
        ]



        with Path(file_path).open('w') as f:
            json.dump(character_dict, f, indent=4)

        print(f"Character saved to {file_path}")

    @classmethod
    def load_from_json(cls, file_path: str) -> 'Character':
        """
        Load a character from a JSON file.

        :param file_path: The path to the JSON file
        :return: A Character instance
        """
        with Path(file_path).open('r') as f:
            character_data = json.load(f)

        # Convert skill category strings back to Enum
        for skill in character_data['skills']:
            skill['category'] = SkillCategory(skill['category'])

        return cls(**character_data)

    def print_character_sheet(self) -> None:
        """
        Prints a basic character sheet.
        """
        sheet = f"""
                ╔{'═' * 50}╗
                ║{self.name:^50}║
                ║{f"Cult Rank: {self.cult_rank}":^50}║
                ╠{'═' * 50}╣
                ║ Characteristics:
                ║ {', '.join([f"{k}: {v}" for stat in self.stats for k, v in stat.items()])}
                ╠{'═' * 50}╣
                ║ Attributes:
                ║ Damage Modifier: {self.damage_modifier}
                ║ Magic Points: {self.magic_points}
                ║ Strike Rank: {self.strike_rank}
                ║ Hit Points by Location:
                ║ {', '.join([f"{loc}: {hp}" for loc, hp in self.hit_points.items()])}
                ╠{'═' * 50}╣
                ║ Skills:
                ║ {', '.join([f"{skill.name}: {skill.value}" for skill in self.skills])}
                ╠{'═' * 50}╣
                ║ Features:
                ║ {', '.join(self.features)}
                ╠{'═' * 50}╣
                ║ Cults:
                ║ {', '.join(self.cults)}
                ╚{'═' * 50}╝
                """
        print(dedent(sheet))


#test = Character.create(name="test", age=30,cult_rank="should not be required", stats=[
       # {"STR": 12}, {"CON": 14}, {"SIZ": 10}, {"DEX": 15},
        #{"INT": 16}, {"POW": 13}, {"CHA": 14}
    #])
#print(test)