# nervous-system

## Using a Distributed Key-Value Store to Manage Platform9 Services

This repo contains config files, code and notes describing a proof-of-concept for using [Hashicorp's Consul](https://www.consul.io/) and [confd](https://github.com/kelseyhightower/confd) as a configuration manager for Platform9 clouds.

## Problem
As a demonstration, I'm using the example of a sudden requirement to update the glance keystone password. Glance (like all of our api services) uses a dedicated user/password to authenticate with keystone in order to validate tokens it receives from api clients. The user associated with this password is an admin on the services project, so if the password is somehow compromised, we'd need to change it in a hurry.

This password is used both on DUs and imagelibrary role hosts, and in both cases it's needed in multiple configuration files. To change it, we'd need to:
* modify the password in keystone
* update the password in the glance-api and glance-registry configuration files on all regions.
* restart all the DU-side glance services.
* push a new configuration to each host where the password is stored in both the imagelibrary and glance-api service configurations.

With our current configuration methods, we'd need to update the password in mongo, and write a special-purpose ansible playbook to update the password in keystone and all the region glance configs. Note that this special playbook would duplicate logic in both the glance and keystone configuration playbooks. Any updates to the structure of the original configuration, e.g. a pull from openstack upstream, would require this extra playbook to be updated as well.

Then to update the configuration on the hosts, we'd need to run a host configuration push through resource manager for each host with the imagelibrary role.

## How it works
For the demo, I've chosen Hashicorp's consul to act as a our distributed key-value store. Consul has nice features for service management, discovery, health monitoring and DNS, but I'm only using key-value storage and 'watches' which allow us to trigger actions on value updates. In addition, I'm using confd, which will render templatized configuration files based on values in the KV store.

With the complete setup, changing the password involves simply changing the password in the configuration store. A change in the store automatically initiates:

* an update to the password in keystone
* newly rendered glance and imagelibrary configuration files.
* restarts of the glance and imagelibrary services in all DUs and hosts.

## DUs and hosts
The demo setup has 2 DUs (regions). The DUs are in our dev ec2:

* The first DU (call it r1) has 3 hosts (h1, h2 and h3). h2 and h3 both have the imagelibrary role enabled.
* the second DU (call it r2) has no hosts.
* in addition I've deployed a third ec2 instance to complete a three-node consul quorum.

## Setup

* Both DUs run consul in 'server' mode along with confd Configuration, code and DU-specific details are in r1/ and r2/ in the repo.
* all three hosts run consul in 'client' mode. Details are in h1/, h2/ and h3/ in the repo.
* consul is started on the the third quorum host with the same command line as r2.

## TODO
A more complete proof of concept would include:

* tunnel consul clients through comms/switcher or some other transport that allows on-premise clients to securely talk to the server cluster.
* use certs and namespacing to limit customers/DUs/hosts access based on need-to-know for configuration values.

## Proposal
Let's do all hosted and on-premise service configuration this way! Also, explore using consul, etc to start, watch and manage services, help with health checking and endpoint discovery.

## Consul References:
* [Securing Consul](https://www.mauras.ch/securing-consul.html)
* [Turning on ACL's in our Consul cluster](http://jovandeginste.github.io/2016/05/04/turning-on-acl-s-in-our-consul-cluster.html)
* [Consul Encryption (Docs)](https://www.consul.io/docs/agent/encryption.html)
* [Digital Ocean etcd/confd/coreos](https://www.digitalocean.com/community/tutorials/how-to-use-confd-and-etcd-to-dynamically-reconfigure-services-in-coreos)
* [Consul iptables rules](http://blog.alexey-plotnik.me/2016/05/23/consul/)
