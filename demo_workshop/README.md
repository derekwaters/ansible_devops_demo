# AAP Workshop Demo

Build an environment for an interactive AAP workshop.

Accompanying slide deck:

https://docs.google.com/presentation/d/1LNetunoLOo7t4k8SSDxV38DCaelR6LvoXSJfGUQUE2s/edit?slide=id.g36affb6d25c_0_96#slide=id.g36affb6d25c_0_96

And workshop instructions:

https://docs.google.com/document/d/1kDdD1ZLV8v3xG3pXrukYC95ykRqNlePXeOv2wN8JBl0/edit?tab=t.0

To deploy:

1) On RHDP create a new "AWS with OpenShift Open Environment":

https://demo.redhat.com/catalog?category=Open_Environments&item=babylon-catalog-prod%2Fsandboxes-gpte.sandbox-ocp.prod

2) Wait for the environment to provision.
3) Ensure you have a ServiceNow developer account and a ServiceNow dev instance (with hostname and password)
4) Install Ansible
5) You need the following collections:

- ansible.controller (available from Red Hat Cloud Console Automation Hub only)
- ansible.eda
- redhat.openshift
- infra.controller_configuration (available from Red Hat Cloud Console Automation Hub only)
- servicenow.itsm

6) Generate an AAP Licensing Manifest File (refer to https://docs.ansible.com/automation-controller/4.4/html/userguide/import_license.html#obtain-sub-manifest for details)
7) Run the following command (substituting your relevant values):

`ansible-playbook -i <inventory_file> -e ocp_host=https://<OpenShift API Hostname>:6443 -e ocp_username=kubeadmin -e ocp_password="<OpenShift Admin Password>" -e ocp_token=<token> -e aap_manifest_path="<Local Path to AAP Manifest ZIP File for Licensing AAP>" -e demo_name=demo_workshop ./playbooks/_deploy_demo_on_ocp.yml`

This will:

1) Install the AAP Operator
2) Install AAP with default settings
3) Obtain the AAP hostname
4) Install EDA referring to the AAP host
5) Retrieve hostnames and admin passwords for both AAP and EDA
6) License AAP with the provided manifest file
7) Create the demo content within AAP
8) Debug out the hostnames and admin passwords for later access
