import yaml

with open("php-apache.yaml", 'r') as testing:
        try:
                print(yaml.safe_load(testing))
                yamlfile = open("php-apache.yaml")
                parsed = yaml.load(yamlfile, Loader=yaml.FullLoader)
                print(parsed['spec']['template']['spec']['containers'][0])
                print(parsed['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'])
        except yaml.YAMLError as exc:
                print(exc)