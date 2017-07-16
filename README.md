# CMDB-ng
An attempt at building a next generation CMDB by a sysadmin

# Idea
Have a central repository to dump JSON blobs to, both tracked and non tracked for changes.
Why JSON? No schema foo! Query for what you want anyway using modern RDBMS that supports JSON natively for querying.
The information is worth a lot more if it is stored in a central manner and updated when the changes occur. Tie in updates in databases with triggers and your central CMDB can be updated practically instantly.

The value of the CMDB is only as good as its sources, so there needs to be a lot of them. There is value in a source and it increases exponentially as you add more. When relating an object to another from different sources, there needs to be established ways of comparing, this needs more investigation to make it dynamic enough. Keyword: GraphQL

# Architecture
Storage: Database
Access: API
Update: MQ / API
Sources: Scripts / daemons that poll / listen for events to trigger updates.
Languages:
* Backend: Python3
* Sources: Any, as long as they can talk to the API or to the MQ.

# Sources
In progress:
- PuppetDB

Planned:
- RackTables
- Cisco Prime

To be written:
- Icinga2
- VMware vCenter
- System Center Virtual Machine Manager
- Active Directory
- DNS:
 - PowerDNS

# Plan
Sources can be done at any time, for 0.1 the idea is to write it as part of verifying the concept.
Sources for VMware vCenter and the like can thus come as soon as the concept is up and running as intended.

## Version 0.1 (Current)
* Proof of concept version to show its usability
* MQ to Database write
* Sources that write to MQ:
  * PuppetDB
  * RackTables

## Version 0.2
* API in place for managing
* MQ to API write

## Version 0.9
* Frontend with PHP-Diff or somesuch to view the data and be able to diff between revisions of objects.

## Version 1.0
