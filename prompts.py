standard_skills = """
    STANDARD_SKILLS = {
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
"""




professional_skills = """
    PROFESSIONAL_SKILLS = {
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
        }"""
        
#from wonderwords import RandomWord
from character_base import Character
import random



#r = RandomWord()


#word1 = r.word(include_parts_of_speech=["adjectives"])
#word2 = r.word(include_parts_of_speech=["nouns"])
#word3 = r.word(include_parts_of_speech=["verb"])

words = "smear campaign occult"

generator_preamble="""
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


stats_system_message = """
###Task
1) 
Distribute 80 points among the six stats to create a character 
for a historical tabletop role-playing game.

2)
Do it step-by-step, trying to capture the essence
of the character.

3)
Respect the maximum and minimum values.

MIN: STR 3,  CON 3,  DEX 3,  POW 3,  CHA 3,  SIZ 8,  INT 8
MAX: STR 18, CON 18, DEX 18, POW 18, CHA 18, SIZ 18, INT 18
4)
Use your tools!
5)
Use calculate_stats first before saving anything. Only use the final_stats 
after you have calculated the stats. 

"""

stats_user_prompt = """
"properties": {
        "name": "Pierre Dupont",
        "age": 35,
        "appearance": {
            "height": 1.75,
            "weight": 68.0,
            "eye_color": "Blue",
            "hair_color": "Brown",
            "description": "Tall and lean, with a neatly trimmed mustache and an air of quiet confidence."
        },
        "occupation": "Baker",
        "background": "Pierre was born into a family of bakers in a small village outside of Paris. After inheriting 
        the family business, he moved to Paris to open a successful bakery known for its baguettes and pastries.",
        "notes": null,
        "gender": "Male",
        "birthplace": "Versailles",
        "current_location": "Paris",
        "education": "Apprenticed under his father",
        "training": ["Baking", "Pastry Making"],
        "hobbies": ["Reading", "Gardening", "Playing the Accordion"],
        "personality_traits": ["Hardworking", "Friendly", "Punctual"],
        "relationships": {
            "wife": "Marie Dupont",
            "children": "Louise Dupont, Jean Dupont"
        }
    }

"""


character_test = """
"properties": {
        "name": "Pierre Dupont",
        "age": 35,
        "appearance": {
            "height": 1.75,
            "weight": 68.0,
            "eye_color": "Blue",
            "hair_color": "Brown",
            "description": "Tall and lean, with a neatly trimmed mustache and an air of quiet confidence."
        },
        "occupation": "Baker",
        "background": "Pierre was born into a family of bakers in a small village outside of Paris. After inheriting 
        the family business, he moved to Paris to open a successful bakery known for its baguettes and pastries.",
        "notes": null,
        "gender": "Male",
        "birthplace": "Versailles",
        "current_location": "Paris",
        "education": "Apprenticed under his father",
        "training": ["Baking", "Pastry Making"],
        "hobbies": ["Reading", "Gardening", "Playing the Accordion"],
        "personality_traits": ["Hardworking", "Friendly", "Punctual"],
        "relationships": {
            "wife": "Marie Dupont",
            "children": "Louise Dupont, Jean Dupont"
        }
    }

"""

generic_preamble = """

### Preamble

You are a skillful and diligent GM assistant who have a british flair to their creativity. Below are your instructions and guidelines
that will help you succeed with your tasks.
"""


SKILLS = """
#SKILLS
##Standard Skills
###Athletics
Athletics covers a range of physical activities, including climbing, jumping, throwing, and running. Skills rolls for any of these activities are handled by a single roll against the Athletics skill. See Movement in the Game System section for more information on climbing, jumping, and running.
###Boating
The Boating skill covers the operation of small floating craft. on rivers, lakes, and close inshore. Appropriate vessels are generally boats, canoes, or rafts which travel short distances and are unsuited to the rigours of the open sea. Most are propelled using oars, paddles, punts or simple sails; or can even be towed by animals. Ships with large crews or designed for long, overseas journeys are covered under the Seamanship Professional Skill.
###Brawn
Brawn is the efficient application of technique when applying raw physical force. The skill covers acts of applied might, including lifting, breaking down doors and contests of strength.
###Combat Style
Each Combat Style is the skill to use the weapons expected of a career or culture in the setting. Most fighting traditions encompass training in multiple weapons, along with the techniques required to use them all effectively, whether singly or in combination. In addition they often assume a situational element, such as fighting as close order infantry or whilst mounted. Combat Styles can be very diverse, ranging from, for example, Gladiatorial Combat all the way to Space Marine Mobile Infantry.
###Conceal
Conceal is the counterpoint to Stealth, being the concealment of large objects rather than the character themselves. For instance, conceal could be used to hide a chariot behind some rocks, or sweep away the wheel ruts it left so its path cannot be tracked. The skill is versatile in application, anything from hiding a scroll in a library to disguising the presence of a trap or secret passage.
###Customs
Customs represents the character’s knowledge of his own community: its social codes, rites, rituals, taboos, and so on. The skill is used when it is essential to accurately interpret or perform any socially important custom or to behave in a particular way.
###Dance
Just about every culture uses dance in some way – either as recreation or as part of important rituals. It might be a court dance, a war dance, or a simple set of movements accompanying a prayer or ceremonial chant. The Dance skill measures a character’s ability to move rhythmically and accurately (to a reasonable degree) when called upon to do so.
###Deceit
Deceit covers all instances where a character attempts to mask the truth and offer a deception of some kind: barefaced lying, misleading a guard, or even bluffing (or cheating) during a card game. The skill also covers instances where hiding true emotions or motives is necessary (feigning pleasure when one is bitterly disappointed perhaps, or attempting to seem welcoming and open when the opposite is true). Deceit forms a counterpart to the Insight skill and can be used to oppose Insight rolls when others are attempting to discern either truth or motive.
##Drive
Drive covers the control of wheeled or drawn vehicles, whether by one or more beasts of burden or powered by more esoteric means, such as chariots, sleds, sail carts, or even gasoline cars. A roll is also necessary if the vehicle being driven is drawn or powered by a means different than the driver is used to (horses instead of oxen, or a motor rather than animals for example). 
##Endurance
Endurance is a character’s capacity to endure physical stress, pain, and fatigue. It measures the body’s ability to deal with potentially damaging or debilitating conditions and is a general gauge of resilience, stamina, and metabolism. Endurance, like its counterpart Willpower, is used in any number of ways, but most specifically to resist the possible effects of injuries, including harmful poisons and disease.
###Evade
Evade is used to escape from observed, impending danger and can be used against Ranged Weapons (by diving for cover, for example), avoiding traps, changing the engagement distance in combat, and generally getting out of the way of a potential physical hazard. It can also be used as a resistance roll for certain types of magic. Using Evade usually leaves the character prone. Those with the Daredevil Combat Style Trait may use Evade to dodge a melee attack without falling prone and, against a ranged attack, they only end up prone if they fail the roll. 
##First Aid
The skill of First Aid measures a character’s ability to treat minor injuries and stabilise more severe ones. First Aid may be applied only once per specific injury and heals 1d3 points of damage. 
###Influence
This is a measurement of a character’s ability to persuade others, through personal charisma, into a desired way of behaving. It is used in a wide variety of situations; from changing someone’s mind, to bribing an official or guard. Influence rolls are typically opposed by the Perception, Willpower, or another Influence skill, depending on the circumstances, and are modified by how much a character is trying to influence behaviour. Attempting to persuade a close friend to loan you their horse may be relatively easy. Getting a usually incorruptible bureaucrat to accept a bribe is more difficult.
###Insight
Insight is the ability to read or intuitively define another’s verbal and non-verbal behaviour (such as body language or the manner of speech) to establish their motives and state of mind. Insight is used to determine whether someone is telling a lie (and it can be opposed by the other person’s Deceit skill), or to predict how someone feels about a particular situation. Insight can equally be applied to particular situations as well as other people: is that tavern a haven for trouble? Could the bandits be planning an ambush in the nearby hills?
###Locale
Locale measures a character’s understanding of local flora, fauna, terrain, and weather in the area where he or she has spent much of their life, usually within their community. The character knows the common plants, trees, and animals, their properties and behaviour: where the best fish can be found; the movements of game creatures; where to find shelter; the likely weather for the season, and the most common regional dangers. In neighbouring, yet unfamiliar locations Locale should be made one or more grades harder.
###Native Tongue
Native Tongue is the ability to speak and read one’s own language, the one learned while growing up in one’s home culture. Native Tongue measures articulation, eloquence, and the depth of the speaker’s vocabulary.
Unlike other skills, Native Tongue is not rolled against directly. Instead, it is treated as a static representation of overall fluency, limiting the level of conversational interaction. This is described in more detail under the Language skill, but starting characters usually begin play fully fluent in their mother tongue.
###Perception
Perception is used for both passive observation and focused detection; whether hunting for something specific, a general scan of an area, or simple awareness of their surroundings. Specific conditions – darkness, for example – may affect the Difficulty Grade of the skill roll depending on the primary senses being used. Strong scents might make an olfactory Perception roll Easy rather than Standard, whereas trying to eavesdrop on a conversation in a crowded and noisy tavern would make the roll Hard.
###Ride
Ride covers the ability to control and remain mounted on those creatures that are trained to be ridden. The skill can be applied to a diverse range of beasts, everything from mules to elephants; even flying or swimming creatures such as giant eagles or dolphins. Riding an unfamiliar species is always one Difficulty Grade harder; while riding a species of a different medium (a horseman riding a dragon, for example) is two grades harder. Wild, untamed creatures cannot be ridden in a constructive manner until they have been broken and trained to be riding beasts.
###Sing
Carrying a tune is covered by Sing, anything from monotonous chants through to complex arias. Singing is an inherent part of most cultures, a prime source of entertainment and perhaps used in its rituals. Important songs might be used for courting, inspiring soldiers before battle, or simply recounting a historical deed. The skill reflects the user’s ability to maintain rhythm, keep in key and remember the correct words.
###Stealth
Hiding out of plain sight, or moving with minimal sound are covered by the Stealth skill. Cover and conditions, such as darkness or loud background noise, improve the grade of the skill according to the specifics of the environment. Similarly, adverse conditions, such as a lack of cover or a quiet night will decrease the skill’s grade. Circumstances also affect the difficulty of the attempt. For instance, a warrior wearing heavy armour can easily conceal themselves behind a wall, provided they stand still or move very slowly, whereas moving quickly might cause their armour to jingle.
###Swim
Without development, the ability to swim is limited to being able to thrash around and keep one’s head above the water for a short time. Higher Swim percentages indicate being able to negotiate deeper and stronger waters, with less risk of drowning. Making a Swim roll thus depends entirely on the conditions. Rough seas, strong currents, white water, and rip tides all reduce the grade of the skill no matter what the character’s affinity for water might be. See Movement for more information on swimming, including calculating swim speeds.
###Unarmed
Unarmed is a universal Combat Skill common to all characters, measuring the ability to defend oneself without the aid of weapons. The Unarmed skill covers the brawling and wrestling techniques known by that culture. 
As Unarmed is a Combat Skill its Critical and Fumble effects are covered by the rules for combat, as detailed in the Combat chapter.
###Willpower
Willpower is a measure of a character’s ability to concentrate, channel his force of will in a particular direction, or harden his psyche to possible mental shock. It is also a measure of personal resolve. The skill is used in all manner of situations where mental resilience is required, and this includes resisting magic. Although not a measure of sanity it can be used to endure traumatic events that would shake even the sanest, stable mind. Willpower is the mental counterpart to Endurance.
Again, like Endurance and Evade, Willpower is most often used in Opposed Rolls. When used as a Standard test, a Critical Willpower roll indicates that the character has hardened his mind and spirit to the extent that no further attempts to influence him, or shake his resolve, will work. In the case of resisting magic, a Critical Success means that no further mentally afflicting spells cast by the opponent have any effect on the character for the remainder of that encounter.
##Professional Skills
Professional Skills differ between characters and represent more specialised forms of training and experience. Some Professional Skills are gathered through cultural background and a character’s Career, as the name suggests. Although they differ between characters they work in the same way as Standard Skills.
###Acting
Acting governs the art of being able to impersonate and convey a completely different character, whether in a staged performance or in a social situation. The actor portrays a personality and mannerisms different to his own in a convincing manner. Coupled with the Disguise and Deceit skills, this is a powerful way of becoming someone else entirely. 
###Acrobatics
Acrobatics covers acts of balance, gymnastics, juggling, and tumbling. The skill can be used to impress an audience, but also to help mitigate damage from falls. With a successful roll, a character can move at full speed and sure-footedly across an unstable or narrow surface. If trying to mitigate damage from an unexpected fall, a successful Acrobatics roll halves any damage sustained. In addition, if the roll is successful and the character does not suffer a Serious or Major Wound due to the fall, the character lands relatively safely and is not prone.
Acrobatics can be substituted for Evade if the situation warrants it. The benefit of this is that the character automatically regains their footing rather than being rendered prone.
###Astrogation
Astrogation is equivalent to Navigation, save that it enables starship pilots to plot a course at stellar and interstellar distances.
###Art
There are many specific art forms. Painting to Poetry; Literature to Sculpture. A character chooses an Art specialisation when taking this skill. Subsequent Art forms are advanced separately. A roll is made whenever a character must impress or convince through his artistic medium.
###Bureaucracy 
Understanding administrative procedures, records, and unspoken conventions are covered by the Bureaucracy skill. It is used to interact with officials or discover pertinent civic information. Depending on the sophistication of their culture, bureaucrats need not necessarily be literate. Whenever red-tape or administrative landscapes need to be navigated, a Bureaucracy roll is necessary.
###Commerce
Commerce is used to evaluate the worth of goods and commodities and to trade them for the best possible price. It is also used to understand the intricacies of business transactions in addition to securing a profit. A further use is in finding the best way to dispose of stolen and illicit goods – again for the best possible price. Commerce is obviously used when trading and it can be opposed by either an opponent’s Commerce skill or Willpower, reflecting the opposing side’s attempts to further the deal in their favour. It is also used to judge the market value of goods, gaining an idea of price, and where it will be best traded.
###Comms
This skill grants the ability to use communications equipment to detect, conceal or block comms traffic. It also grants a chance of cracking encrypted messages (providing the user has access to a code-cracker).
###Computers
Computers reflects the character’s ability to solve complex problems or extract complex information, using computer systems – be it through programming code, detailed use of a particular piece of software, hacking, and even diagnosing/repairing software and hardware problems. General use of computers does not usually require a roll.
###Courtesy
This skill covers understanding how to act appropriately in a social or formal situation: modes of address, rituals, and conventions of behavior, and so forth. It includes everything from who to bow to and when, to how low; from when to use a particular title to when it is appropriate to act informally.
###Craft
Each Craft is a specialised form, and there are as many crafts as there are professions for them. Like Art, Craft is used to create the subject item. How long it takes depends entirely on the nature of the product: weaving a rug takes longer than throwing a pot, for instance, but time is not necessarily the most important factor: it is the skill of the crafter, the quality of the resources and attention to detail.
###Culture
Culture is the more specific form of the Standard Skill of Customs, relating instead to societies foreign to the character’s own. Each Culture skill must be given a particular nation or society to which it applies. Mechanically it works in the same way as the Customs skill.
###Demolitions
This skill permits a character to safely handle and utilise explosive materials, whether setting them up or disarming them.
###Disguise
Effecting a convincing disguise, using appropriate materials (costumes, cosmetics, wigs, or hairpieces), is covered by the Disguise skill. Creating the disguise requires time and attention to detail, as well as access to the right materials to make it convincing. If some, or all, of these elements are not present then the Disguise roll’s Difficulty Grade is made one or more steps harder.
Disguise can be augmented with Acting to enhance the overall effect of a deception (vice versa when performing) and so the two skills are complementary.
###Electronics
This skill allows the user to tinker with, bypass or repair electronic devices. It has many applications, most often to temporarily patch up damaged equipment or replace broken circuits with spares.
###Engineering
The design and building of large-scale structures, from houses to bridges, gates to siege engines, is in the remit of the Engineering skill. Rolls are necessary when planning large-scale projects to ensure correct construction but are also made when an engineer wants to assess a structure’s integrity for whatever reason (state of repair or weak spots, for example).
###Forgery
The Forgery skill permits the creation or falsification of official documentation.
###Gambling
The Gambling skill measures a character’s competence in games of chance and especially where money is staked on the outcome. It is used to assess the odds of success or failure or spot when someone is cheating. The skill can be used in an opposed or unopposed manner, depending on the situation. Spending the night in a faceless gambling den might only require a straight test, whereas a high stakes dice game involving notable personages may instead require several Rounds of Opposed Rolls.
###Healing
Healing is the in-depth knowledge of medical procedures, based on cultural practices and is used to treat more serious injuries (typically those where Hit Points are at zero or less). In a Primitive or Barbarian culture for instance, healing will be based on the knowledge of herbs and natural cures. In a Civilised culture, drugs and more advanced treatments will be more common. In all cultures Healing includes the ability to set bones, suture wounds, and so forth. Obviously applying Healing requires appropriate resources, and most practicing healers will have such things at hand (needles, gut or thread for sutures, herbs for poultices, and so forth, or a medical kit for modern settings). 
###Language
This skill covers the speaking and comprehension of a language other than the character’s own. The skill is treated as a static representation of overall fluency. 1-25% a few basic words, 26-50% simple sentences, 51-75% fluent for general conversation, 76+% able to converse eloquently. Its value is used by the Games Master to limit the level of spoken interaction when the players converse with personalities in the game. It can also be used as a cap for certain other skills (such as Bureaucracy), where Language may be a limiting factor. In such a case, a skill like Bureaucracy cannot exceed the skill value of the Language being used.
###Lockpicking
Lockpicking is the ability to open a mechanical locking system without the aid of a key or other device made specifically for the lock. It includes the techniques of levering open bolted or barred doors and windows without causing damage. Lockpicking may also be used to lock a door, chest, and so on, when no key is available. 
###Lore
Lore covers a specific body of knowledge which must be chosen when the skill is first learned. Alchemy, Astrology, Astronomy, Geography, Heraldry, History, Midwifery, Mineral, Monsters, Politics, Religion, Strategy and Tactics: these are all typical examples of Lore skills. Skill in a Lore means the character understands its fundamentals, how it can be applied to immediate challenges and problems, and can use the Lore to recall useful information. 
###Mechanisms
Mechanisms represents the knowledge and skill to assemble and disassemble mechanical devices, such as traps. The skill of Mechanisms generally involves the creation of delicate contraptions with small working parts, as opposed to Engineering, which deals with massive constructions. It is a distinct discipline from Lockpicking and cannot be interchanged with that skill.
###Musicianship
Musicianship covers the playing of musical instruments; from a simple reed pipe to a complex stringed instrument such as a harp, and each iteration of Musicianship is applied to a group of similar instruments. A musician who can play a reed pipe can also play a flute, panpipes, or a recorder because the fundamentals are the same. They could not, however, play a harp or lute. 
###Navigation 
Whether using prominent landmarks, the stars, or the varying taste of seawater, the ability to accurately direct travel is covered by the Navigation skill. Each Navigation skill covers a specific region or environment, such as Open Seas or Underground for example. It should be made during unusual journeys or when in completely unfamiliar territory.
##Oratory
Oratory is the art of delivering a speech to a large group of people with the aim of conveying or swaying a point of view. It is a skill frequently used by politicians to drive home a policy, but is also used by commanders to inspire troops and impose discipline on the battlefield. Wherever mass persuasion is needed, Oratory, rather than Influence, is used.
###Pilot
The Pilot skill permits the control of a specified class (such as gliders, prop-driven planes, jet engines, and so on) of flying vehicles.
###Politics
Characters possessing the Politics skill understand how to navigate and negotiate the corridors of government at local and national levels.
###Research
Research uses various resources (such as a library, newspaper archive, computer network, and so on), to discover desired pieces of information.
##Science
There are dozens of scientific disciplines and the Science skill, which can be taken multiple times, is always associated with a discipline: Science (Biology) or Science (Chemistry), for example. Science replaces the Lore skill in modern and futuristic settings.
###Seamanship
This skill is used in the same way as Boating but is instead applied to large waterborne vessels powered by sail or banks of oars. It also covers the maintenance and upkeep of a ship: assessing when repairs are needed, where it is safe to anchor, the dangers of violent weather, and so forth.
###Seduction
Seduction is the romantic or sexual persuasion of another person, a skill very different to Influence. It uses explicit signals – verbal and non-verbal – to elicit a sexually positive response. It also takes a significant amount of time: successful Seduction may take hours, days, or weeks to achieve depending on the morals of the target, who can always attempt to resist Seduction with Willpower.
###Sensors
This skill allows the accurate use and analysis of sensor devices from chemical sniffers up to military long range scanners.
###Sleight
Sleight covers attempts to palm or conceal small objects (legerdemain and prestidigitation) and includes attempts to pick pockets, cut purses, or cause a visual distraction. Naturally, it is an essential thieves’ skill.
###Streetwise
Streetwise represents knowledge of places and social contacts within a settlement. It covers everything from identifying potentially dangerous neighbourhoods, to finding local services – legal or illegal. How long a Streetwise attempt takes depends on what is sought. Finding a good inn will take less time than locating a fence for stolen goods or a fake trading permit.
###Survival
This skill covers surviving in a rural or wilderness environment where the benefits of civilisation are absent: foraging, building a fire, finding shelter or a safe place to sleep. When properly equipped, rolls are usually unnecessary since the character may be carrying a tent, food supplies, and so on. Only when separated from their equipment or when environmental conditions turn bad does it become essential to use this skill. A roll is usually made once per day in such conditions.
###Teach
Teach allows the user to pass on their knowledge and techniques in an easy to understand and constructive manner. Without this skill even the most capable of masters will suffer problems instructing others.
###Track
The Track skill is used for tracking any form of game or quarry. It uses both obvious and ambiguous signs of passing to remain on the quarry’s trail, including footprints, bruised leaves, scattered pollen, displaced rocks, and so on; small, tell-tale signs that are invisible to the non-skilled. Track rolls need to be made periodically, especially if conditions change abruptly (a rain shower, for example, will disturb certain signs). How often depends on how cunning the quarry has been. Conceal rolls can be used to oppose a Track roll.
***
"""


system_prompt = SKILLS + generic_preamble


part2a = """
##Format
A list of the nine skills chosen (as strings) in descending order of importance. Please, use
the same spelling as in the STANDARD_SKILLS dictionary.

STANDARD_SKILLS = ["the", "choice", "of", "skills", "in", "descending", "order", "of", "importance"]
"""

part1a = """
###Task
Could you choose nine skills from the provided STANDARD_SKILLS dictionary? Arranging them in descending order of
importance to the character. Please, reason about what experience the character might have. Think step by step and
have some fun with the assignment.

"""

part3a = """
    STANDARD_SKILLS = {
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
"""

standard_prompt = part1a + character_test + part2a + part3a

standard_system_prompt = SKILLS + generic_preamble + part1a + part2a + part3a
part1b = """
###Task
Could you choose six skills from the provided PROFESSIONAL_SKILLS dictionary? Arranging them in descending order of
importance to the character. Please, reason about what areas of expertise the character have. Think step by step and
have some fun with the assignment.

"""

part2b = """
##Format
A list of the six skills chosen (as strings) in descending order of importance.

PROFESSIONAL_SKILLS = ["only", "use", "the", "spelling", "in", "LIST_OF_VALID_PROFESSIONAL_SKILLS"]
"""


part3b = """
    LIST_OF_VALID_PROFESSIONAL_SKILLS = {
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
        }"""
professional_system_prompt = SKILLS + generic_preamble + part1b + part2b + part3b
professional_prompt = part1b + character_test + part2b + part3b
