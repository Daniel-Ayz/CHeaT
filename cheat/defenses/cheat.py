from cheat.defenses.defense_database import DefenseDatabase
from cheat.defenses.defense_creator import DefenseCreator
from cheat.defenses.defense_installer import DefenseInstaller
import random

class CHeaT:
    def __init__(self, database_path, logger):
        self.database = DefenseDatabase(database_path, logger)
        self.logger = logger
        self.creator = DefenseCreator()
        self.installer = DefenseInstaller(logger)

    def plant_defense(self, asset_type, asset_path, technique, method="prompt_injection", template="Combined_Attack"):
        self.logger.info("Planting defense...")
        try:
            if method == "honeytoken":
                all_techniques = self.database._get_honeytoken_defenses()
                all_templates = self.database._get_honeytoken_templates()
            elif method == "prompt_injection":
                all_techniques = self.database._get_promptinjection_defenses()
                all_templates = self.database._get_promptinjection_templates()
            else:
                self.logger.error(f"Unknown method: {method}")
                return

            # Step 3: Choose technique
            if technique == "random":
                technique = random.choice([entry["technique"] for entry in all_techniques])
                self.logger.info(f"Randomly selected technique: {technique}")
                
            # Query DB to extract the technique, template, and method.
            technique_obj = self.database.get_technique_method(technique, method)
            if not technique_obj:
                raise ValueError(f"Technique {technique} with method {method} not found in the database.")

            template_obj = self.database.get_template(template)
            if not template_obj:
                raise ValueError(f"Template {template} not found in the database.")

            # Combine technique with template
            defense_obj = self.creator.combine_template_defense(template_obj, technique_obj, asset_type)

            # Install defense in asset
            install_success = self.installer.install_defense(asset_type, asset_path, defense_obj)

            if install_success:
                self.database.record_installed_defense(asset_type, asset_path, defense_obj)
                self.logger.info(f"Successfully installed {technique_obj['technique']} inside {asset_path} of type {asset_type}.")
            else:
                self.logger.error(f"Failed to install {technique_obj['technique']} inside {asset_path} of type {asset_type}.")
        except Exception as e:
            self.logger.error(f"Error during defense installation: {str(e)}")

    def print_available_defenses(self):
        self.logger.info("Listing all available defenses...")
        try:
            defenses = self.database.get_all_available_defenses()
            if defenses:
                for defense in defenses:
                    self.logger.info(f"Defense: {defense}")
            else:
                self.logger.info("No defenses available in the database.")
        except Exception as e:
            self.logger.error(f"Error fetching available defenses: {str(e)}")

    def print_installed_defenses(self):
        self.logger.info("Listing all installed defenses...")
        try:
            installed_defenses = self.database.get_all_installed_defenses()
            if installed_defenses:
                for defense in installed_defenses:
                    self.logger.info(f"Installed Defense: {defense}")
            else:
                self.logger.info("No defenses installed.")
        except Exception as e:
            self.logger.error(f"Error fetching installed defenses: {str(e)}")

    def remove_all_defenses(self):
        self.logger.info("Removing all defenses...")
        try:
            installed_defenses = self.database.get_all_installed_defenses()
            if not installed_defenses:
                self.logger.info("No defenses to remove.")
                return

            for defense in installed_defenses:
                defense_id = defense["id"]
                asset_type = defense["asset_type"]
                asset_path = defense["asset_path"]

                removal_success = self.installer.remove_defense(asset_type, asset_path, defense)
                if removal_success:
                    self.database.remove_defense(defense_id)
                    self.logger.info(f"Successfully removed defense {defense_id} from {asset_path} of type {asset_type}.")
                else:
                    self.logger.error(f"Failed to remove defense {defense_id} from {asset_path} of type {asset_type}.")
        except Exception as e:
            self.logger.error(f"Error during removal of defenses: {str(e)}")

    def remove_defense(self, defense_id):
        self.logger.info(f"Removing defense {defense_id}...")
        try:
            defense = self.database.get_defense_by_id(defense_id)
            if not defense:
                self.logger.error(f"Defense with ID {defense_id} not found in the database.")
                return

            asset_type = defense["asset_type"]
            asset_path = defense["asset_path"]

            removal_success = self.installer.remove_defense(asset_type, asset_path, defense)
            if removal_success:
                self.database.remove_defense(defense_id)
                self.logger.info(f"Successfully removed defense {defense_id} from {asset_path} of type {asset_type}.")
            else:
                self.logger.error(f"Failed to remove defense {defense_id} from {asset_path} of type {asset_type}.")
        except Exception as e:
            self.logger.error(f"Error during removal of defense {defense_id}: {str(e)}")
