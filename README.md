 [![Build Status](https://travis-ci.com/rolandli2012/Ansible_Automation.svg?branch=master)](https://travis-ci.com/rolandli2012/Ansible_Automation)

# Ansible_Automation

## Ansible module for export Azure Subscription Inventory for playbook. 

The module is using Azure service principal to retrieve the following information from the inventory of the given subsciption:

  * Resouce Groups
  * Virtual Networks
  * Virtual Machines
  * Network Security Groups
  * Subnets
  * Vnics
  * Storage Accounts
  * Storage Blobs

The module supports Python 3.5. It's using Azure sdk for Python, there is an alternate approach by using [Azure REST API](https://docs.microsoft.com/en-us/rest/api/virtualnetwork/subnets/list "Azure REST API - List Subnets")

There is a test subscritpion in the playbook. Azure_Inventory.txt is the output file generated by Ansible based on this test subscription.
