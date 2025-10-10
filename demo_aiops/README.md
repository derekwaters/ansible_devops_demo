# AIOps demo

Deploy AAP with a bunch of setup to demonstrate AAP and OpenShift AI as part of an AIOps setup

This requires additional manual configuration (currently) to set up the Agentic AI / llamastack / MCP / OCP components

***IMPORTANT NOTE*** You can't currently set up OPA config with the ansible collections
so this has to be done manually, as shown below.

To deploy:

1) On RHDP create a new "AWS with OpenShift Open Environment":

https://demo.redhat.com/catalog?category=Open_Environments&item=babylon-catalog-prod%2Fsandboxes-gpte.sandbox-ocp.prod

2) On RHDP create a new "AWS Blank Open Environment":

https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.sandbox-open.prod

3) Wait for the environments to provision.
4) Ensure you have the following tools installed:

* ansible-core
* python3
* pip
* kustomize
* helm
* htpasswd
* oc
* vault
* yq

5) Ensure you have the following collections installed:

- ansible.controller (available from Red Hat Cloud Console Automation Hub only)
- ansible.platform (available from Red Hat Cloud Console Automation Hub only)
- infra.aap_configuration (available from Red Hat Cloud Console Automation Hub only)
- ansible.eda
- redhat.openshift

6) Deploy the OpenShift AI environment using the instructions here:

https://github.com/derekwaters/rhoai-roadshow-v2/tree/main/src/ansible

(this may take a couple of hours)

7) Generate an AAP Licensing Manifest File (refer to https://docs.ansible.com/automation-controller/4.4/html/userguide/import_license.html#obtain-sub-manifest for details)
8) Once your OpenShift Open Environment is provisioned, obtain the API URL and User Access Token
9) Run the following command (substituting your relevant values):

`ansible-playbook -i <inventory_file> -e ocp_host=https://<OpenShift API Hostname>:6443 -e ocp_username=kubeadmin -e ocp_token="<OpenShift Token>" -e aap_manifest_path="<Local Path to AAP Manifest ZIP File for Licensing AAP>" -e -e demo_name=demo_aiops ./playbooks/_deploy_demo_on_ocp.yml`

This will:

* Install the AAP Operator
* Install AAP 2.6 with gateway, controller and EDA
* License AAP with the provided manifest file
* Create the demo content within AAP*
* Install the OpenPolicyAgent as a container in the 'opa' namespace
* Debug out the AAP URL and admin passwords for later access

It doesn't (currently) set up the link between AAP and OPA as the Ansible collections do not yet support the opa_query_path parameter.

10) Open AAP and go to the Settings -> Policy page.
11) Edit the Settings
12) Set the hostname to the hostname of the OPA service on the OpenShift cluster (TODO: Find out what this is by default)
13) Save the Settings
14) Add the policy path 'aap_tests/allowed' to the 'midrange-vms' Inventory.
15) Obtain an API Token and API Access URL from AAP
16) Set the API Access env vars:

export AAP_TOKEN=ABCDEF...
export AAP_URL="https://my-aap-server.com/"

17) Deploy the MCP server by running:

oc login <details of the OpenShift cluster hosting AAP>
oc apply -f demo_aiops/mcp_server/mcp_resources.yml

18) Get the full URL from the Route for later:

oc get route route-mcp-server-aap -n mcp

19) Log in to the Openshift AI cluster:

oc login <OpenShift AI Cluster login details>
oc project llama-stack

20) Run the AI agent in an interactive temporary container:

oc run agentic-test-sample -ti --image=quay.io/rh-ee-dwaters/agentic-aap-demo:latest --rm=true --restart=Never \ 
	--env="LLAMASTACK_URL=http://llamastack-with-config-service.llama-stack.svc.cluster.local:8321" \
	--env="REMOTE_AAP_MCP_URL=http://<MCP_SERVER_ROUTE_OBTAINED_EARLIER>/sse" \
	--env="LLAMASTACK_MODEL_ID=deepseek/deepseek-r1-0528-qwen3-8b-bnb-4bit" -- \
	/bin/bash

21) Once the container starts and you get a bash prompt, run:

python agentic-aap-demo.py

22) Ask away! A good sample prompt is:

Find a job template to solve the following error: '{ "type": "error", "host": "app-db-02", "message": "Disk /data is 95% full. Please ensure this device has sufficient space" }' If you find a solution, launch the job template with the relevant inventory. If you need an incident number, obtain one with the create_incident tool. 