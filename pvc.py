from kubernetes import client, config

def main():
    config.load_kube_config(config_file='./config.yaml')
    api = client.CoreV1Api()
    
    pvcs = api.list_namespaced_persistent_volume_claim(namespace='default', watch=False)
    
    for pvc in pvcs.items:
        print(pvc.metadata.name, pvc.spec.volume_name, pvc.spec.resources.requests['storage'])
                
if __name__ == '__main__':
    main()