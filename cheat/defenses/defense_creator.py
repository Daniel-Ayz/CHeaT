class DefenseCreator:
    def __init__(self):
        pass

    def combine_template_defense(self, template, defense, asset_type):
        """
        Combines a template and defense into a formatted prefix and suffix, adjusted for the asset type.
        """
        raw_prefix = template["Injection_Template"].replace("<OBJECTIVE>", defense["Injection_Task"])
        raw_suffix = defense["Injection_Suffix"]

        # Adjust the prefix and suffix based on the asset type
        if asset_type == "local_file":
            return {
                "prefix": f"{raw_prefix}\n",
                "suffix": f"\n{raw_suffix}"
            }
        elif asset_type == "web_file":
            return {
                "prefix": f"<!-- {raw_prefix} -->\n",
                "suffix": f"\n<!-- {raw_suffix} -->"
            }
        elif asset_type == "tool_wrapper":
            return {
                "prefix": raw_prefix,
                "suffix": raw_suffix
            }
        else:
            raise ValueError(f"Unknown asset type: {asset_type}")
