# Developer Hub running Automation demo

This demo shows Developer Hub with GPTs to deploy infra using AAP automation

Accompanying slide deck:

<<<TODO>>>

To deploy:

1) On RHDP create a new "AWS with OpenShift Open Environment":

https://demo.redhat.com/catalog?category=Open_Environments&item=babylon-catalog-prod%2Fsandboxes-gpte.sandbox-ocp.prod

2) Wait for the environment to provision.
3) Ensure you have a ServiceNow developer account and a ServiceNow dev instance (with hostname and password)
4) Install Ansible
5) You need the following collections:

- ansible.controller (available from Red Hat Cloud Console Automation Hub only)
- ansible.eda (available from Red Hat Cloud Console Automation Hub only)
- redhat.openshift
- infra.aap_utilities (available from Red Hat Cloud Console Automation Hub only)
- infra.controller_configuration (available from Red Hat Cloud Console Automation Hub only)

6) Generate an AAP Licensing Manifest File (refer to https://docs.ansible.com/automation-controller/4.4/html/userguide/import_license.html#obtain-sub-manifest for details)
7) Run the following command (substituting your relevant values):

`ansible-playbook -i <inventory_file> -e ocp_host=https://<OpenShift API Hostname>:6443 -e ocp_username=kubeadmin -e ocp_password="<OpenShift Admin Password>" -e aap_manifest_path="<Local Path to AAP Manifest ZIP File for Licensing AAP>" -e snow_hostname="https://<ServiceNow_instance_hostname>" -e snow_password="<ServiceNow_admin_password>" -e demo_name=demo_devhub ./playbooks/_deploy_demo_on_ocp.yml`


This will:

1) Install the AAP Operator
2) Install AAP with default settings
3) Obtain the AAP hostname
4) Install EDA referring to the AAP host
5) Retrieve hostnames and admin passwords for both AAP and EDA
6) License AAP with the provided manifest file
7) Create the demo content within AAP (linked to ServiceNow)
8) Debug out the hostnames and admin passwords for later access
