import flywheel
import os
from Template_Project import TemplateProject
import logging
from pathlib import Path
logging.basicConfig(level="DEBUG")


def main():
    BASE_DIR = Path(__file__).resolve().parents[1]
    print(BASE_DIR)
    template_project_id = "640a167feec1e8ab7317cf89"
    dest_project_id = "64400ef073c2f0c4d5203349"
    api_key = os.environ["NACC_API"]
    client = flywheel.Client(api_key)
    project = client.get_project(template_project_id)
    template_project = TemplateProject(client, project)

    dest_project = client.get_project(dest_project_id)
    template_project.copy_all_rules_to_project(dest_project)


# template_project.copy_rule_to_project("form-validator", dest_project)


if __name__ == "__main__":
    main()
