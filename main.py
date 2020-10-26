from __future__ import print_function
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config, utils
import json
import requests
import yamlpullk8s
import sys,time
from os import path
import logging
import deployment_crud

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


def kube_list_namespace_deployment():
    with kubernetes.client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = kubernetes.client.AppsV1Api(api_client)
        namespace = 'default'  # str | object name and auth scope, such as for teams and projects
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    allow_watch_bookmarks = True  # bool | allowWatchBookmarks requests watch events with type \"BOOKMARK\". Servers that do not implement bookmarks may ignore this flag and bookmarks are sent at the server's discretion. Clients should not assume bookmarks are returned at any specific interval, nor may they assume the server will send any BOOKMARK event during a session. If this is not a watch, this field is ignored. If the feature gate WatchBookmarks is not enabled in apiserver, this field is ignored.  This field is beta. (optional)
    _continue = '_continue_example'  # str | The continue option should be set when retrieving more results from the server. Since this value is server defined, kubernetes.clients may only use the continue value from a previous query result with identical query parameters (except for the value of continue) and the server may reject a continue value it does not recognize. If the specified continue value is no longer valid whether due to expiration (generally five to fifteen minutes) or a configuration change on the server, the server will respond with a 410 ResourceExpired error together with a continue token. If the kubernetes.client needs a consistent list, it must restart their list without the continue field. Otherwise, the kubernetes.client may send another list request with the token received with the 410 error, the server will respond with a list starting from the next key, but from the latest snapshot, which is inconsistent from the previous list results - objects that are created, modified, or deleted after the first list request will be included in the response, as long as their keys are after the \"next key\".  This field is not supported when watch is true. Clients may start a watch from the last resourceVersion value returned by the server and not miss any modifications. (optional)
    field_selector = ''  # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
    label_selector = ''  # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
    limit = 56  # int | limit is a maximum number of responses to return for a list call. If more items exist, the server will set the `continue` field on the list metadata to a value that can be used with the same initial query to retrieve the next set of results. Setting a limit may return fewer than the requested amount of items (up to zero items) in the event all requested objects are filtered out and kubernetes.clients should only use the presence of the continue field to determine whether more results are available. Servers may choose not to support the limit argument and will return all of the available results. If limit is specified and the continue field is empty, kubernetes.clients may assume that no more results are available. This field is not supported if watch is true.  The server guarantees that the objects returned when using continue will be identical to issuing a single list call without a limit - that is, no objects created, modified, or deleted after the first request is issued will be included in any subsequent continued requests. This is sometimes referred to as a consistent snapshot, and ensures that a kubernetes.client that is using limit to receive smaller chunks of a very large result can ensure they see all possible objects. If objects are updated during a chunked list the version of the object that was present at the time the first list result was calculated is returned. (optional)
    resource_version = ''  # str | When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv. (optional)
    timeout_seconds = 56  # int | Timeout for the list/watch call. This limits the duration of the call, regardless of any activity or inactivity. (optional)
    watch = True  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

    try:
        api_response = api_instance.list_namespaced_deployment(namespace, pretty=pretty,
                                                               allow_watch_bookmarks=allow_watch_bookmarks,
                                                               _continue=_continue, field_selector=field_selector,
                                                               label_selector=label_selector, limit=limit,
                                                               resource_version=resource_version,
                                                               timeout_seconds=timeout_seconds, watch=watch)
        print(api_response)
    except ApiException as e:
        print("Exception when calling AppsV1Api->list_namespaced_deployment: %s\n" % e)

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


def main():

    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    print("IP Add\t\t Namespace\t\t Name")
    for i in ret.items:
        print("%s\t\t%s\t\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    print('----------------------')
    ###################################################
    resp = requests.get(configuration.host + '/apis/metrics.k8s.io/v1beta1/pods', verify=False)
    resp2= requests.get(configuration.host + '/apis/metrics.k8s.io/v1beta1/nodes', verify=False)
    print(resp.text)
    print(resp2.text)



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
    main()
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