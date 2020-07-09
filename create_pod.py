from kubernetes import client, config
from datetime import datetime
import time
import random

def get_pod(name, data):
    return {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name
            },
            "spec": {
                "containers": [
                    {
                        "name": "sleep",
                        "image": "busybox",
                        "args": [
                            "/bin/sh",
                            "-c",
                            "echo $SOME_ID; sleep 5;"
                        ],
                        "env": [
                            {
                                "name": "SOME_ID",
                                "value": f"{data}"
                            }
                        ]
                    }
                ],
                "restartPolicy": "Never"
            }
        }

def main():
    namespace = 'python'
    config.load_kube_config(config_file='./config.yaml')
    api = client.CoreV1Api()

    date = datetime.now().strftime('%H%M')    
    name = f'test-{date}'
    data = random.randint(0, 20)
    pod_data = get_pod(name, data)
    
    resp = api.create_namespaced_pod(namespace, body=pod_data)
    while True:
        resp = api.read_namespaced_pod(name=name,
                                       namespace=namespace)
        if resp.status.phase != 'Pending':
            break
        time.sleep(1)
    print('Done.')
                
if __name__ == '__main__':
    main()