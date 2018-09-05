#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: azure_inventry

short_description: This is Azure Inventry module

version_added: "2.4"

description:
    - "This module uses Azure Python SDK to query Azure Subscription Inventory. The module is using service principal to access Azure resources"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Roland Li
'''

EXAMPLES = '''
- name: Output Azure Subscription Inventory using azure_inventory 
  azure_inventory:
    subscription: "{{ subscription }}"
    tenant: "{{ tenant }}"
    client: "{{ client }}"
    secret: "{{ secret }}"
'''

RETURN = '''
response:
    description: Response specific to subscription.
    returned: always
    type: dict
'''

import os
from ansible.module_utils.basic import AnsibleModule
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient

def run_module():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
     
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        subscription=dict(type='str', required=True),
        tenant=dict(type='str', required=True),
        client=dict(type='str', required=True),
        secret=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    subscription_id = module.params['subscription']
    TENANT_ID = module.params['tenant']
    CLIENT = module.params['client']
    KEY = module.params['secret']

    credentials = ServicePrincipalCredentials(
        client_id = CLIENT,
        secret = KEY,
        tenant = TENANT_ID
    )

    resource_client = ResourceManagementClient(credentials,subscription_id)
    compute_client = ComputeManagementClient(credentials,subscription_id)
    network_client = NetworkManagementClient(credentials,subscription_id)
    storage_client = StorageManagementClient(credentials,subscription_id)

    GROUP_NAME = ''
    
    print_file('Azure Subscription Inventory Report\n\nList Subscription\n')
    for item in resource_client.resource_groups.list():
        print_file("\tName: {}\n".format(item.name))
        print_file("\tId: {}\n".format(item.id))
        print_file("\tLocation: {}\n\n".format(item.location))
        GROUP_NAME = item.name

    # List VM in resource group
    print_file("\nList VMs in resource group\n")
    for vm in compute_client.virtual_machines.list(GROUP_NAME):
        print_file("\tVM: {}\n\n".format(vm.name))

    # List Virtual Network in resource group
    print_file("\nList Virtual Network in resource group\n")
    for vnet in network_client.virtual_networks.list(GROUP_NAME):
        print_file("\tVirtual Network: {}\n".format(vnet.name))

        # List Subnets in resource group
        print_file("\nList Subnets in {}\n".format(vnet.name))
        for subnets in network_client.subnets.list(GROUP_NAME, virtual_network_name=vnet.name):
            print_file("\tSubnets: {}\n".format(subnets.name))

    # List Network Security Groups in resource group
    print_file("\nList Network Groups in resource group\n")
    for nsgroup in network_client.network_security_groups.list(GROUP_NAME):
        print_file("\tNetwork Security Groups: {}\n".format(nsgroup.name))

    # List Vnics in resource group
    print_file("\nList Vnics in resource group\n")
    for nics in network_client.network_interfaces.list(GROUP_NAME):
        print_file("\tNetwork Interface Card: {}\n".format(nics.name))

    # List Storage Accounts in resource group
    for accounts in storage_client.storage_accounts.list():
        print_file("\nList Storage Accounts")
        print_file("\tStorage Account: {}\n".format(accounts.name))

        # List Storage Blobs in resource group
        for blobs in storage_client.blob_containers.list(GROUP_NAME, account_name=accounts.name).value:
            print_file("\nList Storage Blobs in {}\n".format(accounts.name))
            print_file("\tStorage Blob: {}\n".format(blobs.name))

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

def print_file(s):
    file = open("Azure_Inventory.txt","a")
    file.write(s)
    file.close()

if __name__ == '__main__':
    main()
