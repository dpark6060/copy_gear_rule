import flywheel
import logging

log = logging.getLogger()


class TemplateProject:
    def __init__(self, client: flywheel.Client, project: flywheel.Project):
        self.client = client
        self.project = project
        self.rules = self._load_rules_from_template_project()

    def _load_rules_from_template_project(self):
        return self.client.get_project_rules(self.project.id)

    def get_rule(self, rule_name):
        rule = [r for r in self.rules if r.name == rule_name]
        return rule[0]

    def copy_all_rules_to_project(self, dest_project):
        for rule in self.rules:
            self.copy_rule_to_project(rule.name, dest_project)

    def copy_rule_to_project(self, rule_name, dest_project):
        log.info(f"copying rule {rule_name}")
        rule = self.get_rule(rule_name)
        dest_files = self.handle_rule_files(rule, dest_project)
        gri = self.create_rule_input_object(rule, dest_files)
        self.client.add_project_rule(dest_project.id, gri)
        log.info("done")

    def handle_rule_files(self, rule, dest_project):
        files = rule.fixed_inputs
        dest_files = []
        for file in files:
            file_object = self.project.get_file(file.name)

            if not self.same_file_exists(file_object, dest_project):
                self.copy_file_to_dest(file_object, dest_project)

            dest_files.append(
                {
                    "id": dest_project.id,
                    "input": file.input,
                    "name": file.name,
                    "type": file.type,
                    "version": file.version,
                }
            )
        return dest_files

    @staticmethod
    def copy_file_to_dest(file_object, dest_project):
        file_spec = flywheel.FileSpec(
            file_object.name, file_object.read(), file_object.mimetype
        )
        dest_project.upload_file(file_spec)

    @staticmethod
    def same_file_exists(file_object, dest_project):
        dest_file = dest_project.get_file(file_object.name)
        if not dest_file:
            log.debug(
                f"No File {file_object.name} on destination project {dest_project.label}, uploading"
            )
            return False

        if dest_file.hash == file_object.hash:
            log.debug(
                f"File {file_object.name} on destination project {dest_project.label} matches hash of original file, no changes"
            )
            return True

        log.debug(
            f"File {file_object.name} on destination project {dest_project.label} does not match hash of original file, updating"
        )
        return False

    @staticmethod
    def create_rule_input_object(rule, dest_files):
        dict_rule = rule.to_dict()
        dict_rule["fixed_inputs"] = dest_files
        gear_rule_keys = flywheel.GearRuleInput().keys()
        dict_rule = {k: v for k, v in dict_rule.items() if k in gear_rule_keys}
        gri = flywheel.GearRuleInput(**dict_rule)
        return gri
