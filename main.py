import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client
import datetime, time
import simulatefail as podmgr
import virtualboxcont

configuration = kubernetes.client.Configuration()
api_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Im1EZGVmMUVxaGVkOTVvZllZM0JWR2RFS0hrcnVRamM3MUk1eVNMOEgwQ1UifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNDUyaGgiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjczNTUxNWViLWRlMzEtNDFhNy04YjFkLWI3MjVhODRkNTJiNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.OjyfzkwLNw1tZhDPhsRhV4dBFtoPuzZDYvhDb3soB83Do60H8CkihfsTegPbTKqRxxdFeRMR4pylFNSDkeFbxXOk0JsT7uh7IjUEiqk7dCaScdO5r-oEO1r3ENxgdbHafRl6QqPQxuIpF8-ifAJHLKSkJQ6AOhwtTA05ddTGLdZ--t0A2POp_6-GG-ZoXI_yHCShiccBlaIWjlAxt_XQNAE0ALszka5uJwTRKHRIdV3XmATRY__C3KOY2sOPyJdNCrfHPsK_r86pHk2CQoK1EojTlh6TkDIQ53koaF7kJ0x1EB6btLoFlPa6xvk1-FD3pCFaqgfVilZwQ1uebFqDKA'
configuration.api_key = {"authorization": "Bearer " + api_token}
configuration.host = "https://192.168.1.240:6443"
configuration.verify_ssl = False
configuration.assert_hostname = False
configuration.debug = False

apiclient = client.ApiClient(configuration)

input_from_usr = ""
listofpods = [None]*10
listvm = [None]*20

def main():
    while(1):
        print("Enter number to execute function:")
        input_from_usr = input("(1) Choose and delete pods (2) Choose and pause nodes (3) Choose and resume nodes\n")
        if (input_from_usr == '1'): # Kill pods section
            while (input_from_usr != "exit"):
                print("List of pods to kill for default namespace. Type 'exit' to quit pod deletion")
                v1 = client.CoreV1Api(apiclient)
                ret = v1.list_namespaced_pod(watch=False, namespace="default", pretty=False)
                count = 1
                print("No\t Name\t\t\t\t\t\t\t Status\t\t Time")
                for i in ret.items:
                    listofpods[count] = i.metadata.name
                    print("(%d)  %s\t %s\t %s" % (count, i.metadata.name, podmgr.get_pod_status(i.metadata.name), podmgr.query_start_time(i.metadata.name)))
                    count += 1
                try:
                    input_from_usr = input("Alternatively, type (%d) or Enter to Refresh.: " % (count))
                    if (input_from_usr == "exit"):
                        break
                    elif (input_from_usr == str(count) or input_from_usr == ''):
                        print("Refreshing...")
                        print("-------------------------------------------------------------------------------------")
                        continue
                    else:
                        podmgr.delete_pod(listofpods[int(input_from_usr)])
                        time.sleep(1)

                except ApiException as E:
                    print("Wrong value entered or not found")

        elif (input_from_usr == '2'):
            while (input_from_usr != "exit"):
                print("List of VM to pause")
                count = 1
                for m in virtualboxcont.vbox.machines:
                    listvm[count] = m
                    print("(%d) %s" % (count, listvm[count]))
                    count += 1
                try:
                    input_from_usr = input()
                    if (input_from_usr == "exit"):
                        break;
                    virtualboxcont.pause_machine(str(listvm[int(input_from_usr)]))
                    print("VM %s paused at %s" % (listvm[int(input_from_usr)], datetime.time))
                    time.sleep(1)
                except ApiException as exc:
                    print("Wrong value entered or not found")

        elif (input_from_usr == '3'):
            while (input_from_usr != "exit"):
                print("List of VM to pause")
                count = 1
                for m in virtualboxcont.vbox.machines:
                    listvm[count] = m
                    print("(%d) %s" % (count, listvm[count]))
                    count += 1
                try:
                    input_from_usr = input()
                    if (input_from_usr == "exit"):
                        break;
                    virtualboxcont.resume_machine(str(listvm[int(input_from_usr)]))
                    print("VM %s resumed at %s" % (listvm[int(input_from_usr)], datetime.time))
                    time.sleep(1)
                except ApiException as exc:
                    print("Wrong value entered or not found")

        else:
            print("Invalid input")



if __name__ == '__main__':
    main()