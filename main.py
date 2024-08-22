import urwid
import time
from generator import CharacterGenerator
from character_base import Character
from prompts import generator_preamble, paris_prompt, stats_system_message, standard_system_prompt, professional_system_prompt
from naming import get_random_female_name, get_random_male_name, load_name_data
import json
import os

current_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(current_dir, 'name_1940.csv')


with open(csv_file_path, 'r') as file:
    # Process the CSV file
    name_data = file.read()
    
def generate_random_neworleans(stats_user_prompt: str, base_character: dict = None):
    creator = CharacterGenerator(
        generator_preamble,
        paris_prompt,
        stats_system_message,
        standard_system_prompt,
        professional_system_prompt
    )
    return creator.create_character_from_description(stats_user_prompt, base_character)



class CharacterGeneratorApp:
    def __init__(self):
        self.current_character = None
        self.main_screen = self.create_main_screen()
        self.character_screen = None
        self.optional_details_screen = None
        self.optional_details = {}
        self.main_widget = None  # Initialize this in the run method
        
    def show_initial_loading_screen(self, message="Starting the process..."):
        text = urwid.Text(message, align='center')
        loading_widget = urwid.Filler(text, valign='middle')
        self.loop.widget = loading_widget
        self.loop.draw_screen()
        


    
    def create_main_screen(self):
        title = urwid.BigText("Character Generator", urwid.font.HalfBlock5x4Font())
        title = urwid.Padding(title, 'center', width='clip')
        title = urwid.AttrMap(title, 'title')
        
        create_player_character_button = urwid.Button("👤 Create Player Character", on_press=self.show_player_character_form)
        generate_male_button = urwid.Button("♂ Generate Male Character", on_press=self.generate_male_character)
        generate_female_button = urwid.Button("♀ Generate Female Character", on_press=self.generate_female_character)
        generate_custom_button = urwid.Button("✎ Generate Custom Character", on_press=self.show_optional_details_screen)
        display_button = urwid.Button("👁 Display Current Character", on_press=self.display_character)
        quit_button = urwid.Button("✖ Quit", on_press=self.exit_program)

        buttons = [generate_male_button, generate_female_button, generate_custom_button, create_player_character_button, display_button, quit_button]
        button_pile = urwid.Pile([urwid.AttrMap(b, 'button', focus_map='reversed') for b in buttons])
        button_box = urwid.LineBox(button_pile, title="Menu Options")

        content = urwid.Pile([
            ('pack', title),
            ('pack', urwid.Divider()),
            ('weight', 1, button_box),
        ])
        return urwid.Padding(content, left=2, right=2)
    
    def show_player_character_form(self, button):
        self.player_character_form = self.create_player_character_form()
        self.loop.widget = self.player_character_form

    def create_player_character_form(self):
        title = urwid.Text(("title", "Create Player Character"))
        
        form_fields = [
            ('Name', urwid.Edit),
            ('Gender', urwid.Edit),
            ('Age', urwid.IntEdit),
            ('Height', urwid.Edit),
            ('Weight', urwid.Edit),
            ('Eye Color', urwid.Edit),
            ('Hair Color', urwid.Edit),
            ('Appearance', urwid.Edit),
            ('Cult Rank', urwid.Edit),
            ('Occupation', urwid.Edit),
            ('Background', urwid.Edit),
            ('Birthplace', urwid.Edit),
            ('Current Location', urwid.Edit),
            ('Education', urwid.Edit),
            ('Training', urwid.Edit),
            ('Hobbies', urwid.Edit),
            ('Personality Traits', urwid.Edit),
            ('Family Relationships', urwid.Edit),
            ('Notes', urwid.Edit),
        ]

        self.form_widgets = {}
        form_items = []
        for label, widget_class in form_fields:
            if widget_class == urwid.IntEdit:
                edit = widget_class(caption=f"{label}: ")
            else:
                edit = widget_class(f"{label}: ")
            self.form_widgets[label] = edit
            form_items.append(edit)

        submit_button = urwid.Button("Create Character", on_press=self.create_player_character)
        back_button = urwid.Button("Back to Main Menu", on_press=self.show_main_screen)

        form_content = urwid.Pile(form_items + [urwid.Divider(), submit_button, back_button])
        form_padding = urwid.Padding(form_content, left=2, right=2)
        return urwid.Frame(header=title, body=urwid.ListBox(urwid.SimpleListWalker([form_padding])))

    def create_player_character(self, button):
        character_data = {}
        for label, widget in self.form_widgets.items():
            if isinstance(widget, urwid.IntEdit):
                value = widget.value()
                if value is not None:
                    character_data[label.lower().replace(' ', '_')] = value
            else:
                value = widget.edit_text.strip()
                if value:  # Only add non-empty string values
                    if label in ['Training', 'Hobbies', 'Personality Traits']:
                        value = [item.strip() for item in value.split(',') if item.strip()]
                    elif label == 'Family Relationships':
                        value = {f'Relationship {i+1}': rel.strip() for i, rel in enumerate(value.split(',')) if rel.strip()}
                    
                    character_data[label.lower().replace(' ', '_')] = value

        if not character_data:
            self.show_error("Please fill in at least one field before creating a character.")
            return

        # Generate stats and skills
        stats_prompt = f"Generate stats and skills for a character with the following details: {json.dumps(character_data)}"
        self.generate_character(stats_prompt, base_character=character_data)

    def generate_character(self, custom_prompt, base_character=None):
        self.show_initial_loading_screen("Preparing character generation...")
        self.loop.set_alarm_in(0.1, self.start_character_generation, (custom_prompt, base_character))

    def start_character_generation(self, loop, user_data):
        custom_prompt, base_character = user_data
        self.show_loading_screen()
        try:
            character = generate_random_neworleans(custom_prompt, base_character)
            if isinstance(character, Character):
                self.current_character = character.__dict__
            else:
                self.show_error("Failed to generate a valid character.")
                return
            self.display_character(None)
        except Exception as e:
            self.show_error(f"Error generating character: {str(e)}")

    def show_initial_loading_screen(self, message):
        text = urwid.Text(message, align='center')
        loading_widget = urwid.Filler(text, valign='middle')
        self.loop.widget = loading_widget
        self.loop.draw_screen()



    def create_optional_details_screen(self):
        title = urwid.Text(("title", "Custom Character Details"))
        self.location_edit = urwid.Edit("Location: ")
        self.profession_edit = urwid.Edit("Profession: ")
        self.other_edit = urwid.Edit("Other details: ")
        
        gender_group = []
        self.male_radio = urwid.RadioButton(gender_group, "Male")
        self.female_radio = urwid.RadioButton(gender_group, "Female")

        generate_button = urwid.Button("Generate Character", on_press=self.generate_custom_character)
        back_button = urwid.Button("Back to Main Menu", on_press=self.show_main_screen)

        content = urwid.Pile([
            ('pack', title),
            ('pack', urwid.Divider()),
            ('pack', urwid.Text("Optional Details (leave blank if not needed):")),
            ('pack', self.location_edit),
            ('pack', self.profession_edit),
            ('pack', self.other_edit),
            ('pack', urwid.Divider()),
            ('pack', urwid.Text("Select Gender:")),
            ('pack', self.male_radio),
            ('pack', self.female_radio),
            ('pack', urwid.Divider()),
            ('pack', urwid.AttrMap(generate_button, 'button', focus_map='reversed')),
            ('pack', urwid.AttrMap(back_button, 'button', focus_map='reversed'))
        ])
        return urwid.Padding(urwid.LineBox(content), left=2, right=2)

    def show_optional_details_screen(self, button):
        self.optional_details_screen = self.create_optional_details_screen()
        self.loop.widget = self.optional_details_screen

    def generate_male_character(self, button):
        name = get_random_male_name(name_data)
        self.generate_character(f"Generate a male character named {name}.", None)

    def generate_female_character(self, button):
        name = get_random_female_name(name_data)
        self.generate_character(f"Generate a female character named {name}.", None)


    def generate_custom_character(self, button):
        location = self.location_edit.edit_text.strip()
        profession = self.profession_edit.edit_text.strip()
        other = self.other_edit.edit_text.strip()
        
        if self.male_radio.state:
            gender = "male"
        elif self.female_radio.state:
            gender = "female"
        else:
            self.show_error("Please select a gender.")
            return

        name = get_random_male_name(name_data) if gender == "male" else get_random_female_name(name_data)
        
        custom_prompt = f"Generate a {gender} character named {name}"
        if location:
            custom_prompt += f" from {location}"
        if profession:
            custom_prompt += f" working as a {profession}"
        if other:
            custom_prompt += f". Additional details: {other}"
        custom_prompt += "."

        self.generate_character(custom_prompt, None)


    def start_character_generation(self, loop, user_data):
        custom_prompt, base_character = user_data
        self.show_loading_screen()
        try:
            character = generate_random_neworleans(custom_prompt, base_character)
            if isinstance(character, Character):
                self.current_character = character.__dict__
            else:
                self.show_error("Failed to generate a valid character.")
                return
            self.display_character(None)
        except Exception as e:
            self.show_error(f"Error generating character: {str(e)}")
    def show_loading_screen(self):
        text = urwid.Text("Generating character...", align='center')
        loading_bar = urwid.ProgressBar('body', 'progress')
        content = urwid.Pile([text, loading_bar])
        loading_screen = urwid.Filler(content, valign='middle')
        self.loop.widget = loading_screen

        def update_progress(progress):
            loading_bar.set_completion(progress)
            if progress < 100:
                next_progress = min(progress + 2, 100)
                self.loop.set_alarm_in(0.05, lambda loop, user_data: update_progress(next_progress))
            else:
                self.loop.set_alarm_in(0.5, lambda loop, user_data: self.display_character(None))

        self.loop.set_alarm_in(0.1, lambda loop, user_data: update_progress(0))

        def update_progress(progress):
            loading_bar.set_completion(progress)
            if progress < 100:
                self.loop.set_alarm_in(0.05, lambda loop, user_data: update_progress(progress + 2))
            else:
                self.loop.widget = self.character_screen

        self.loop.set_alarm_in(0.1, lambda loop, user_data: update_progress(0))

    def display_character(self, button):
        if self.current_character:
            self.character_screen = self.create_character_screen(self.current_character)
            self.loop.widget = self.character_screen
        else:
            self.show_error("No character generated yet. Please generate a character first.")
    

    def format_character_text(self, character_data):
        formatted_lines = []

        def add_section(title, content, color='section_title'):
            formatted_lines.extend([
                (color, f"\n{title}\n"),
                (color, "=" * len(title) + "\n"),
            ])
            if isinstance(content, dict):
                for key, value in content.items():
                    formatted_lines.extend([
                        ('key', f"{key}: "),
                        ('value', f"{value}\n")
                    ])
            elif isinstance(content, list):
                for item in content:
                    formatted_lines.append(('value', f"• {item}\n"))
            else:
                formatted_lines.append(('value', f"{content}\n"))
            formatted_lines.append(('value', "\n"))

        # Basic Information
        # Basic Information
        basic_info = {
            "Name": character_data.get("name", "N/A"),
            "Gender": character_data.get("gender", "N/A"),
            "Age": character_data.get("age", "N/A"),
            "Occupation": character_data.get("occupation", "N/A"),
            "Birthplace": character_data.get("birthplace", "N/A"),
            "Current Location": character_data.get("current_location", "N/A")
        }
        add_section("Basic Information", basic_info, 'section_title_1')

        # Background
        add_section("Background", character_data.get("background", "N/A"), 'section_title_2')

        # Education and Training
        edu_training = {
            "Education": character_data.get("education", "N/A"),
            "Training": ", ".join(character_data.get("training", [])) if character_data.get("training") else "N/A"
        }
        add_section("Education and Training", edu_training, 'section_title_1')

        # Personality and Hobbies
        personality_hobbies = {
            "Personality Traits": ", ".join(character_data.get("personality_traits", [])) if character_data.get("personality_traits") else "N/A",
            "Hobbies": ", ".join(character_data.get("hobbies", [])) if character_data.get("hobbies") else "N/A"
        }
        add_section("Personality and Hobbies", personality_hobbies, 'section_title_2')

        # Relationships
        add_section("Relationships", character_data.get("family_relationships", "N/A"), 'section_title_1')

        # Stats
        stats = character_data.get("stats", [])
        if isinstance(stats, list):
            stats = {k: v for d in stats for k, v in d.items()}
        add_section("Stats", stats, 'section_title_2')

        # Skills
        skills = character_data.get("skills", [])
        if isinstance(skills, list):
            skills = {skill.name: skill.value for skill in skills}
        add_section("Skills", skills, 'section_title_1')

        # Attributes
        attributes = character_data.get("attributes", None)
        if attributes:
            attributes_dict = {
                "Action Points": attributes.action_points,
                "Damage Modifier": attributes.damage_modifier,
                "Magic Points": attributes.magic_points,
                "Strike Rank": attributes.strike_rank,
                "Movement": attributes.movement
            }
            add_section("Attributes", attributes_dict, 'section_title_2')

        # Hit Locations
        hit_locations = character_data.get("hit_locations", [])
        if hit_locations:
            hit_loc_formatted = [f"{loc.name} ({loc.range}): HP {loc.hp}, AP {loc.ap}" for loc in hit_locations]
        else:
            hit_loc_formatted = ["N/A"]
        add_section("Hit Locations", hit_loc_formatted, 'section_title_1')

        # Notes
        add_section("Notes", character_data.get("notes", "N/A"), 'section_title_2')

        return formatted_lines

    def create_character_screen(self, character_dict):
        def create_section(title, content, color='section_title'):
            header = urwid.AttrMap(urwid.Text(title), color)
            if isinstance(content, dict):
                body = urwid.Pile([urwid.Text([('key', f"{k}: "), ('value', f"{v}")]) for k, v in content.items()])
            elif isinstance(content, list):
                body = urwid.Pile([urwid.Text(f"• {item}") for item in content])
            else:
                body = urwid.Text(str(content))
            return urwid.LineBox(urwid.Pile([header, body]))

        # Basic Information
        basic_info = create_section("📌 Basic Information", {
            "Name": character_dict.get("name", "N/A"),
            "Gender": character_dict.get("gender", "N/A"),
            "Age": character_dict.get("age", "N/A"),
            "Occupation": character_dict.get("occupation", "N/A"),
            "Birthplace": character_dict.get("birthplace", "N/A"),
            "Current Location": character_dict.get("current_location", "N/A")
        }, 'section_title_1')

        # Background
        background = create_section("📜 Background", character_dict.get("background", "N/A"), 'section_title_2')

        # Education and Training
        edu_training = create_section("🎓 Education and Training", {
            "Education": character_dict.get("education", "N/A"),
            "Training": ", ".join(character_dict.get("training", [])) if character_dict.get("training") else "N/A"
        }, 'section_title_1')

        # Personality and Hobbies
        personality_hobbies = create_section("😊 Personality and Hobbies", {
            "Personality Traits": ", ".join(character_dict.get("personality_traits", [])) if character_dict.get("personality_traits") else "N/A",
            "Hobbies": ", ".join(character_dict.get("hobbies", [])) if character_dict.get("hobbies") else "N/A"
        }, 'section_title_2')

        # Relationships
        relationships = create_section("👥 Relationships", character_dict.get("family_relationships", "N/A"), 'section_title_1')

        # Stats
        stats = character_dict.get("stats", [])
        if isinstance(stats, list):
            stats = {k: v for d in stats for k, v in d.items()}
        stats_section = create_section("📊 Stats", stats, 'section_title_2')

        # Skills
        skills = character_dict.get("skills", [])
        if isinstance(skills, list):
            skills = {skill.name: skill.value for skill in skills}
        skills_section = create_section("🛠 Skills", skills, 'section_title_1')

        # Attributes
        attributes = character_dict.get("attributes", None)
        if attributes:
            attributes_dict = {
                "Action Points": attributes.action_points,
                "Damage Modifier": attributes.damage_modifier,
                "Magic Points": attributes.magic_points,
                "Strike Rank": attributes.strike_rank,
                "Movement": attributes.movement
            }
        else:
            attributes_dict = {"N/A": "N/A"}
        attributes_section = create_section("⚡ Attributes", attributes_dict, 'section_title_2')

        # Hit Locations
        hit_locations = character_dict.get("hit_locations", [])
        if hit_locations:
            hit_loc_formatted = [f"{loc.name} ({loc.range}): HP {loc.hp}, AP {loc.ap}" for loc in hit_locations]
        else:
            hit_loc_formatted = ["N/A"]
        hit_locations_section = create_section("🎯 Hit Locations", hit_loc_formatted, 'section_title_1')

        # Notes
        notes_section = create_section("📝 Notes", character_dict.get("notes", "N/A"), 'section_title_2')

        # Create two columns
        col1 = urwid.Pile([basic_info, background, edu_training, personality_hobbies, relationships])
        col2 = urwid.Pile([stats_section, skills_section, attributes_section, hit_locations_section, notes_section])

        columns = urwid.Columns([col1, col2])

        # Create a ListBox for scrolling
        listbox_content = urwid.SimpleListWalker([columns])
        listbox = urwid.ListBox(listbox_content)

        # Add a title and a back button
        title = urwid.AttrMap(urwid.Text("Character Details", align='center'), 'title')
        back_button = urwid.AttrMap(urwid.Button("Back to Main Menu", on_press=self.show_main_screen), 'button', focus_map='reversed')

        # Combine all widgets
        content = urwid.Frame(
            header=title,
            body=listbox,
            footer=back_button
        )

        return urwid.LineBox(content)

    def show_main_screen(self, button):
        self.loop.widget = self.main_screen

    def show_error(self, message):
        error_text = urwid.Text(('error', message))
        done_button = urwid.Button("OK", on_press=self.show_main_screen)
        content = urwid.Pile([error_text, urwid.AttrMap(done_button, 'button', focus_map='reversed')])
        error_screen = urwid.Filler(content, valign='middle')
        self.loop.widget = error_screen

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            self.exit_program(None)
        elif key in ('m', 'M'):
            self.show_main_screen(None)
        return True

    def run(self):
        palette = [
        ('body', 'dark cyan', ''),
        ('title', 'white,bold', 'dark blue'),
        ('button', 'light gray', 'dark blue'),
        ('reversed', 'standout', ''),
        ('key', 'light cyan', ''),
        ('value', 'light gray', ''),
        ('error', 'light red', 'black'),
        ('progress', 'dark magenta', ''),
        ('section_title', 'yellow,bold', ''),
        ('section_title_1', 'light green,bold', ''),
        ('section_title_2', 'light magenta,bold', ''),
    ]

        header = urwid.AttrMap(urwid.Text("Character Generator", align='center'), 'title')
        footer = urwid.AttrMap(urwid.Text("Q: Quit  |  M: Main Menu", align='center'), 'title')

        self.main_widget = urwid.Frame(
            body=self.main_screen,
            header=header,
            footer=footer
        )

        self.loop = urwid.MainLoop(
            self.main_widget,
            palette=palette,
            unhandled_input=self.unhandled_input
        )

        # Ensure that the main widget is set before running the loop
        if self.loop.widget is None:
            self.loop.widget = self.main_widget

        self.loop.run()


if __name__ == "__main__":
    app = CharacterGeneratorApp()
    app.run()