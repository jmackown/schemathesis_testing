import yaml
import json
with open("static/schema.yml", 'r') as yaml_in, open("static/schema.json", "w") as json_out:
    yaml_object = yaml.safe_load(yaml_in)
    json.dump(yaml_object, json_out)
