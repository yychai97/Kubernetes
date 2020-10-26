"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""
import kubernetes
from kubernetes import client, config

DEPLOYMENT_NAME = "nginx-deployment"


def create_deployment_object(name, image, app_label, replica_no, port, cpu_req, mem_req, cpu_lim, mem_lim, affkey,
                             affvalues):
    # Configureate Pod template container
    container = client.V1Container(name=name,
                                   image=image,
                                   ports=[client.V1ContainerPort(container_port=port)],
                                   resources=client.V1ResourceRequirements(requests={"cpu": cpu_req,
                                                                                     "memory": mem_req},
                                                                           limits={"cpu": cpu_lim,
                                                                                   "memory": mem_lim}))
    # Create and configurate a spec section
    affinity = client.V1PodAntiAffinity(
        preferred_during_scheduling_ignored_during_execution=client.V1WeightedPodAffinityTerm(weight=100,
                                                                                              pod_affinity_term=client.V1PodAffinityTerm(
                                                                                                  client.V1LabelSelector(
                                                                                                      match_expressions=
                                                                                                      {"key": affkey,
                                                                                                       "operator": "In",
                                                                                                       "values": affvalues}),
                                                                                                  topology_key="kubernetes.io/hostname"))
    )
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": app_label}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=replica_no,
        template=template,
        selector={'matchLabels': {'app': app_label}})
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))


def update_deployment(api_instance, deployment, newimage):
    # Update container image
    deployment.spec.template.spec.containers[0].image = newimage
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))


def delete_deployment(api_instance):
    # Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))


def main():
    api_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjBRZDIyWUhqQmJQLThHM2pndl93djBuazRucXVkZVh6U1BiclNwQVJrdWMifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tem13Z2giLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjI3YTAzMmEwLTNjM2UtNGNlOC05MmY1LWYxMTBkNWM1MGVjNiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.u0mDrFD3kPit7FaUIeTnjh1Ph9EGk-s_T4Rn5CRub_WCZ9M31Y4uWkFFK4Sdibez4Lea7maW4J9nq2SP0zoLWxxGgD1aR4ZK2qqyD2QmwfOzUdPdkK1ubII2GZMld5DPbrelA2F58DoFOrwkj_YDNmdZ-pSe1etTWcG4Q_KCoaMSUyDDNa-ZFeKjn8LAoWk1VckW-pSYIq2RcUbbdgHeURfY_qXr0G42eyC7tWnTGZK-k3ZxWneRFAc6fAF0JQD8x6QTMsxH2fc9XFM5yAnniSW2T_oaPF1HgzuMJxATQlTZZT25CwFQcgQwhExH81p8RDjzCLCAP_APRq7fiItyRQ"
    configuration = kubernetes.client.Configuration()
    configuration.api_key = {"authorization": "Bearer " + api_token}
    configuration.host = "https://192.168.1.123:6443"
    configuration.verify_ssl = False
    # configuration.assert_hostname = False
    configuration.debug = True
    ApiClient = client.ApiClient(configuration)

    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    #    config.load_kube_config(ApiClient)
    apps_v1 = client.AppsV1Api(ApiClient)

    # Uncomment the following lines to enable debug logging
    # c = client.Configuration()
    # c.debug = True
    # apps_v1 = client.AppsV1Api(api_client=client.ApiClient(configuration=c))

    # Create a deployment object with client-python API. The deployment we
    # created is same as the `nginx-deployment.yaml` in the /examples folder.
    deployment = create_deployment_object()
    # create_deployment(apps_v1, deployment)
    update_deployment(apps_v1, deployment)


# delete_deployment(apps_v1)


if __name__ == '__main__':
    main()
