import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client
import datetime
from pytz import timezone
import requests
import json
import urllib3

timeformat = "%d-%m-%Y %I:%M:%S %p"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

configuration = kubernetes.client.Configuration()
api_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Im1EZGVmMUVxaGVkOTVvZllZM0JWR2RFS0hrcnVRamM3MUk1eVNMOEgwQ1UifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNDUyaGgiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjczNTUxNWViLWRlMzEtNDFhNy04YjFkLWI3MjVhODRkNTJiNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.OjyfzkwLNw1tZhDPhsRhV4dBFtoPuzZDYvhDb3soB83Do60H8CkihfsTegPbTKqRxxdFeRMR4pylFNSDkeFbxXOk0JsT7uh7IjUEiqk7dCaScdO5r-oEO1r3ENxgdbHafRl6QqPQxuIpF8-ifAJHLKSkJQ6AOhwtTA05ddTGLdZ--t0A2POp_6-GG-ZoXI_yHCShiccBlaIWjlAxt_XQNAE0ALszka5uJwTRKHRIdV3XmATRY__C3KOY2sOPyJdNCrfHPsK_r86pHk2CQoK1EojTlh6TkDIQ53koaF7kJ0x1EB6btLoFlPa6xvk1-FD3pCFaqgfVilZwQ1uebFqDKA'
configuration.api_key = {"authorization": "Bearer " + api_token}
configuration.host = "https://192.168.1.240:6443"
configuration.verify_ssl = False
configuration.assert_hostname = False
configuration.debug = False

apiclient = client.ApiClient(configuration)
v1 = client.CoreV1Api(apiclient)
v1pods = client.V1Pod(apiclient)


def delete_pod(name, ns: str = "default", label_selector: str = "name in ({name})"):
    with kubernetes.client.ApiClient(configuration) as api_client:
        api_instance = client.CoreV1Api(api_client)
        body = kubernetes.client.V1DeleteOptions()  # V1DeleteOptions |  (optional)
    try:
        api_response = api_instance.delete_namespaced_pod(name, ns, body=body, pretty=False)
        print("Pod %s deleted at %s" % (name, datetime.datetime.now()))
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

def list_all_pods_all_namespaces():

    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def list_pods_for_default_namespace():
    #print("Listing pods with default namespace with their IPs:")
    print("Name\t\t\t\t\t\t IP\t\t\t\t Status\t\t Time")
    ret = v1.list_namespaced_pod(watch=False,namespace="default",pretty=False)
    for i in ret.items:
        print("%s\t %s\t %s\t %s\t" % (i.metadata.name, i.status.pod_ip, get_pod_status(i.metadata.name), query_start_time(i.metadata.name)))

def query_start_time(podname):
    try:
        api_response = requests.get(configuration.host + "/api/v1/namespaces/default/pods/"+ podname +"/status", verify=False)
        responses = json.loads(api_response.text)
        dates = responses['metadata']['creationTimestamp']
        dates_utc = datetime.datetime.strptime(dates, "%Y-%m-%dT%H:%M:%SZ")
        dates_kl = dates_utc.astimezone(timezone('Etc/GMT+8'))
        formattedtime = dates_kl.strftime(timeformat)

        return formattedtime

    except ApiException as E:
        print("Issues happend")

def get_pod_status(podname):
    try:
        api_response = requests.get(configuration.host + "/api/v1/namespaces/default/pods/" + podname + "/status",
                                    verify=False)
        responses = json.loads(api_response.text)
        statusofpod = responses['status']['phase']

        return statusofpod
    except ApiException as E:
        print("Error getting status")

    #except ApiException as E:
     #   print("Error cannot get status")



#def main():


if __name__ == '__main__':
    #watch_query_start_time()
    #main()
    #list_all_pods_all_namespaces()
    list_pods_for_default_namespace()

