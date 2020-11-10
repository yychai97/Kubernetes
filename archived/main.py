from __future__ import print_function
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client
from archived import yamlpullk8s
import sys
from os import path
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

configuration = kubernetes.client.Configuration()
#first cluster api token
#api_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Im1EZGVmMUVxaGVkOTVvZllZM0JWR2RFS0hrcnVRamM3MUk1eVNMOEgwQ1UifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNDUyaGgiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjczNTUxNWViLWRlMzEtNDFhNy04YjFkLWI3MjVhODRkNTJiNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.OjyfzkwLNw1tZhDPhsRhV4dBFtoPuzZDYvhDb3soB83Do60H8CkihfsTegPbTKqRxxdFeRMR4pylFNSDkeFbxXOk0JsT7uh7IjUEiqk7dCaScdO5r-oEO1r3ENxgdbHafRl6QqPQxuIpF8-ifAJHLKSkJQ6AOhwtTA05ddTGLdZ--t0A2POp_6-GG-ZoXI_yHCShiccBlaIWjlAxt_XQNAE0ALszka5uJwTRKHRIdV3XmATRY__C3KOY2sOPyJdNCrfHPsK_r86pHk2CQoK1EojTlh6TkDIQ53koaF7kJ0x1EB6btLoFlPa6xvk1-FD3pCFaqgfVilZwQ1uebFqDKA'
#second cluster api token
api_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjBRZDIyWUhqQmJQLThHM2pndl93djBuazRucXVkZVh6U1BiclNwQVJrdWMifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tem13Z2giLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjI3YTAzMmEwLTNjM2UtNGNlOC05MmY1LWYxMTBkNWM1MGVjNiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.u0mDrFD3kPit7FaUIeTnjh1Ph9EGk-s_T4Rn5CRub_WCZ9M31Y4uWkFFK4Sdibez4Lea7maW4J9nq2SP0zoLWxxGgD1aR4ZK2qqyD2QmwfOzUdPdkK1ubII2GZMld5DPbrelA2F58DoFOrwkj_YDNmdZ-pSe1etTWcG4Q_KCoaMSUyDDNa-ZFeKjn8LAoWk1VckW-pSYIq2RcUbbdgHeURfY_qXr0G42eyC7tWnTGZK-k3ZxWneRFAc6fAF0JQD8x6QTMsxH2fc9XFM5yAnniSW2T_oaPF1HgzuMJxATQlTZZT25CwFQcgQwhExH81p8RDjzCLCAP_APRq7fiItyRQ"

configuration.api_key = {"authorization": "Bearer " + api_token}

#first cluster host ip
#configuration.host = "https://192.168.1.240:6443"
#second cluster host ip
configuration.host = "https://192.168.1.123:6443"

configuration.verify_ssl = False
#configuration.assert_hostname = False
configuration.debug = True

#api_instance = kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(configuration))
api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
#api_instance = kubernetes.client.AutoscalingV1Api(kubernetes.client.ApiClient(configuration))
ApiClient = client.ApiClient(configuration)

v1 = client.CoreV1Api(ApiClient)
v1app = client.AppsV1Api(ApiClient)




def kube_test_credentials(): #(/)
    try:
        api_response = api_instance.get_api_resources()
        logging.info(api_response)
    except ApiException as e:
        print("Exception when calling API: %s\n" % e)


def kube_add_deployment(filename): #create_namespaced_deployment (/)
    with open(path.join(path.dirname(__file__), filename)) as f:
        dep = yamlpullk8s.safe_load(f)
        resp = v1app.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % resp.metadata.name)

def kube_update_deployment(filename): #create_namespaced_deployment
    with open(path.join(path.dirname(__file__), filename)) as f:
        dep = yamlpullk8s.safe_load(f)
        resp = v1app.patch_namespaced_deployment(name='php-apache',
            body=filename, namespace="default")
        print("Deployment updated. status='%s'" % resp.metadata.name)



#working
def create_service(names, ports, target_ports): #(/)
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=names
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "deployment"},
            ports=[client.V1ServicePort(
                port=ports,
                target_port=target_ports
            )]
        )
    )
    # Creation of the Deployment in specified namespace
    # (Can replace "default" with a namespace you may have created)
    v1.create_namespaced_service(namespace="default", body=body)


#def main():

    #print("Listing pods with their IPs:")
    #ret = v1.list_pod_for_all_namespaces(watch=False)
    #print("IP Add\t\t Namespace\t\t Name")
    #for i in ret.items:
     #   print("%s\t\t%s\t\t%s" %
     #         (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    #print('----------------------')
    ###################################################
    #resp = requests.get(configuration.host + '/apis/metrics.k8s.io/v1beta1/pods', verify=False)
    #resp2= requests.get(configuration.host + '/apis/metrics.k8s.io/v1beta1/nodes', verify=False)
    #print(resp.text)
    #print(resp2.text)



    ###############################################

  #  pod_name = "counterstrike-868668b69b-pnwq8"
   # try:
  #      api_instance = client.CoreV1Api(ApiClient)
   #     api_response = api_instance.read_namespaced_pod_log(name=pod_name, namespace='default')
  #      print(api_response)
   #     api_response = api_instance.read_node(name='msi1-virtual-machine',exact= True, export=True)
   #     print(api_response)
   # except ApiException as e:
   #     print('Found exception in reading the logs')

#######################################################
def init_hpa(self, tosca_kube_obj, kube_obj_name):
        scaling_props = tosca_kube_obj.scaling_object
        hpa = None
        if scaling_props:
            min_replicas = scaling_props.min_replicas
            max_replicas = scaling_props.max_replicas
            cpu_util = scaling_props.target_cpu_utilization_percentage
            deployment_name = kube_obj_name

            # Create target Deployment object
            target = client.V1CrossVersionObjectReference(
                api_version="extensions/v1beta1",
                kind="Deployment",
                name=deployment_name)
            # Create the specification of horizon pod auto-scaling
            hpa_spec = client.V1HorizontalPodAutoscalerSpec(
                min_replicas=min_replicas,
                max_replicas=max_replicas,
                target_cpu_utilization_percentage=cpu_util,
                scale_target_ref=target)
            metadata = client.V1ObjectMeta(name=deployment_name)
            # Create Horizon Pod Auto-Scaling
            hpa = client.V1HorizontalPodAutoscaler(
                api_version="autoscaling/v1",
                kind="HorizontalPodAutoscaler",
                spec=hpa_spec,
                metadata=metadata)
        return hpa
#####################################################

if __name__ == '__main__':
    #main()
    #create_service("tester")
    kube_add_deployment("php-apache.yaml")
    #kube_update_deployment("php-apache.yaml")
    #kube_list_namespace_deployment()

 #   kube_test_credentials()
  #  kube_cleanup_finished_jobs()
   # kube_delete_empty_pods()

#    for i in range(3):
 #       kube_create_jobs()
  #      logging.info("Finished! - ENV: {}".format(os.environ["VAR"]))
   # sys.exit(0)




#pods = json.loads(resp.text)
 #   max_pods_length =(len(pods['items']))
  #  print(max_pods_length)
   # for i in range(max_pods_length):
    #    print(str(pods[i]))