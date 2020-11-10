import yaml
from archived import deployment_crud


def grab_data_deployment_and_deploy(filename):
    with open(filename, 'r') as testing:
        try:
            print(yaml.safe_load(testing))
            yamlfile = open(filename)
            parsed = yaml.load(yamlfile, Loader=yaml.FullLoader)
            deploymentname=parsed['metadata']['name']
            name=deploymentname
            image=parsed['spec']['template']['spec']['containers'][0]['image']
            app_label=parsed['spec']['template']['metadata']['labels']['app']
            replica_no=parsed['spec']['replicas']
            port=parsed['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort']
            cpu_req=parsed['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu']
            #mem_req=parsed['spec']['template']['spec']['containers'][0]['resources']['requests']['mem']
            cpu_lim=parsed['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu']
            #mem_lim=parsed['spec']['template']['spec']['containers'][0]['resources']['limits']['mem']
            affkey=parsed['spec']['template']['spec']['affinity']['podAntiAffinity']['preferredDuringSchedulingIgnoredDuringExecution'][0]['podAffinityTerm']['labelSelector']['matchExpressions'][0]['key']
            affvalues=parsed['spec']['template']['spec']['affinity']['podAntiAffinity']['preferredDuringSchedulingIgnoredDuringExecution'][0]['podAffinityTerm']['labelSelector']['matchExpressions'][0]['values'][0]
            print(parsed['spec']['template']['spec']['containers'][0])
            print(parsed['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'])
            print(name +" "+ image + " " + app_label+ " " + str(replica_no)+ " " + str(port) +" " + cpu_req + " " + cpu_lim +" " + affkey + " "+ affvalues)
            deployment_crud.create_deployment_object(deploymentname, name, image, app_label, replica_no, port, cpu_req, mem_req=, )
        except KeyError:
                print("Variable not found. Continuing to others")
                pass
        except yaml.YAMLError as exc:
            print(exc)

def grab_data_service_and_deploy(filename):

def grab_data_hpa_and_deploy(filename):

grab_data_deployment_and_deploy("php-apache.yaml")
