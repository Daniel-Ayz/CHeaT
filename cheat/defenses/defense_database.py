import json
import os

HONEYTOKENS_DEFENSES = "honeytokens_defenses.json"
HONEYTOKENS_TEMPLATES = "honeytokens_templates.json"
PROMPT_INJECTION_DEFENSES = "prompt_injection_defenses.json"
PROMPT_INJECTION_TEMPLATES = "prompt_injection_templates.json"
INSTALLED_DEFENSES = "installed_defenses.json"

class DefenseDatabase:
    def __init__(self, db_path, logger):
        self.db_path = db_path
        self.installed_defenses_path = os.path.join(db_path, INSTALLED_DEFENSES)
        self.logger = logger
        # Ensure the installed defenses file exists
        if not os.path.exists(self.installed_defenses_path):
            with open(self.installed_defenses_path, 'w') as f:
                json.dump([], f, indent=4)

    def get_defense_by_id(self, defense_id):
        installed_defenses = self._read_database(INSTALLED_DEFENSES)
        for defense in installed_defenses:
            if defense.get("id") == defense_id:
                return defense
        return None

    def get_all_available_defenses(self):
        honeytoken_defenses = self._get_honeytoken_defenses()
        prompt_injection_defenses = self._get_promptinjection_defenses()
        return honeytoken_defenses + prompt_injection_defenses

    def get_all_installed_defenses(self):
        return self._read_database(INSTALLED_DEFENSES)

    def get_technique_method(self, technique, method):
        all_defenses = self.get_all_available_defenses()
        for defense in all_defenses:
            if defense.get("technique") == technique and defense.get("method", "").lower() == method.lower():
                return defense
        return None

    def get_template(self, template):
        if template is None:
            return None
        honeytoken_templates = self._get_honeytoken_templates()
        prompt_injection_templates = self._get_promptinjection_templates()
        all_templates = honeytoken_templates + prompt_injection_templates
        for tmpl in all_templates:
            if tmpl.get("injection_variant") == template:
                return tmpl
        return None

    def record_installed_defense(self, asset_type, asset_path, defense_obj):
        installed_defenses = self._read_database(INSTALLED_DEFENSES)
        new_defense_entry = {
            "id": self._generate_defense_id(),
            "asset_type": asset_type,
            "asset_path": asset_path,
            **defense_obj
        }
        installed_defenses.append(new_defense_entry)
        self._write_database(INSTALLED_DEFENSES, installed_defenses)
    
    def remove_defense(self, defense_id):
        """
        Removes a defense from the installed defenses database based on its ID.
        """
        try:
            # Read the installed defenses
            installed_defenses = self._read_database(INSTALLED_DEFENSES)
            
            # Filter out the defense with the specified ID
            updated_defenses = [defense for defense in installed_defenses if defense.get("id") != defense_id]
            
            if len(installed_defenses) == len(updated_defenses):
                raise ValueError(f"Defense with ID {defense_id} not found in the database.")
            
            # Write the updated list back to the database
            self._write_database(INSTALLED_DEFENSES, updated_defenses)
            
            self.logger.info(f"Defense with ID {defense_id} successfully removed from the database.")
        except Exception as e:
            self.logger.info(f"Error while removing defense with ID {defense_id}: {str(e)}")

    def _get_honeytoken_defenses(self):
        return self._read_database(HONEYTOKENS_DEFENSES)

    def _get_honeytoken_templates(self):
        return self._read_database(HONEYTOKENS_TEMPLATES)

    def _get_promptinjection_defenses(self):
        return self._read_database(PROMPT_INJECTION_DEFENSES)

    def _get_promptinjection_templates(self):
        return self._read_database(PROMPT_INJECTION_TEMPLATES)

    def _read_database(self, file_path):
        try:
            with open(os.path.join(self.db_path, file_path), 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_database(self, file_path, data):
        with open(os.path.join(self.db_path, file_path), 'w') as file:
            json.dump(data, file, indent=4)

    def _generate_defense_id(self):
        # Generate a unique ID for the defense
        from uuid import uuid4
        return str(uuid4())
