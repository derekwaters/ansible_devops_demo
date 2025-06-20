[Tasks]

oc apply -f containergroup-sa.yml
oc login ------
oc project aap-exec

# Create a one-year long-lived token
oc create token containergroup-service-account --duration=$((365*24))h > containergroup-sa.token
# Maybe this right?
oc extract secret/serving-cert --keys=tls.crt --to=- -n openshift-apiserver > containergroup-sa.ca.crt
oc -n openshift-ingress-operator get secret router-ca -o jsonpath='{.data.tls\.crt}' | base64 -d > ca.crt

Create an OCP API Token credential in AAP
Then create a ContainerGroup with the API url and token (cert only needed if you turn on Verify SSL)
MAKE SURE you customise the pod spec to change the namespace and the serviceAccountName (containergroup-service-account)

# TODO TODO TODO TODO TODO
# 
# Create an SA and ClusterRoleBinding (cluster-admin) for inventory refresh
# Then a token for it too
# Need to generate an ssh token and add the private key as the SSH Machine Credential for access to VMs, then need
# to add the public key as a secret in the VM namespace:


kind: Secret
apiVersion: v1
metadata:
  name: fedora-vm-ssh-access-key
  namespace: sleeper
data:
  key: c3NoLXJzYSBBQUFBQjNOemFDMXljMkVBQUFBREFRQUJBQUFCZ1FEZ3VnZVRPR1NhY0hqdjFTTEdQSkhXV0M2R1ZGVEtlTDBsY1hsVHpiamlmQktZQ05PUE1BMlkrSVJjUWhwcnVhaDg3VGJ4M3VzU0tQa0ttRkl0bjFWM1UrcjJpS1dmSys1cnFHUkJkZTMwVWVZL0pXS0puSExxVUd6cGYzdVhXVDZDcENiTktqZ1BXdWxIbEZuVHZhMVR2bWF6RVhvbnh0MWI1TGN6RUEwQ3gzMTV4YnJNVUF1N01tdHhNSnVCeUkzSmoyZkZRMmJLWDVVSTRhV1hmQWlOc2JxVkJnTitnQ3V6bDV2WGl1czBXc3N1dERvSlJXRmxaclZiYTlKRXdDdkdvZHdVdzA2dWEwYmpkdStSMWU3UmxObURUQ2lxTkNTaEdzenp5SDE1UjlVWFNCR3MreFgwNi9NVGtJM0ZLVE5HWG9SM1Y5cnBjdDJwUUFzOVV4cktWcW1jRjlJRVZ6ODJkRDNiSklyZHhJbmZsVGg2N1R0aXZDeVJBUUYvQzc3MDU4WUROUzdKcllaT0I0aWZzRURTRk9tWGlSRVd3RFpIRWxwWmdKTUNVVEhxeEQ3NkJBYTNXYmF1bW5XZG9HaVhXbTVjKzd5NHJKTmxLcEhoL1NhOFhMZXg3MVNQZExPSVRTYW1yTE5DamdIQk9zK3VIT0F0Q2NiSitsaG05NEU9
type: Opaque

# How is this configured as the default ssh key for all VMs added to the cluster? Bryon is looking into it


# Need to extract the cert for access to the Kafka cluster!!




:: The below doesn't work because there is no token automatically created any more...
:: 
export SA_SECRET=$(oc get sa containergroup-service-account -o json | jq '.secrets[0].name' | tr -d '"')
oc get secret $(echo ${SA_SECRET}) -o json | jq '.data.".dockercfg"' | xargs | base64 --decode > containergroup-sa.token
