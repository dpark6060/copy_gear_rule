import flywheel
import os
from Template_Project import TemplateProject
import logging

logging.basicConfig(level="DEBUG")


def main():
    template_project_id = "63a49440e087afb85232ab00"
    dest_project_id = "63751acb4d4fb3ab518cc50e"
    api_key = os.environ["NACC_API"]
    client = flywheel.Client(api_key)
    project = client.get_project(template_project_id)

    template_project = TemplateProject(client, project)

    dest_project = client.get_project(dest_project_id)
    template_project.copy_all_rules_to_project(dest_project)


# template_project.copy_rule_to_project("form-validator", dest_project)


if __name__ == "__main__":
    main()
