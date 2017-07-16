# CMDB-ng
An attempt at building a next generation CMDB by a sysadmin

# Idea
Have a central repository to dump JSON blobs to, both tracked and non tracked for changes.
Why JSON? No schema foo! Query for what you want anyway using modern RDBMS that supports JSON natively for querying.
The information is worth a lot more if it is stored in a central manner and updated when the changes occur. Tie in updates in databases with triggers and your central CMDB can be updated practically instantly.

The value of the CMDB is only as good as its sources, so there needs to be a lot of them. There is value in a source and it increases exponentially as you add more, when relating an object to another from different sources, there needs to be established ways of comparing.

# Architecture
Storage: Database
Access: API
Update: MQ / API
Sources: Scripts / daemons that poll / listen for events to trigger updates.

# Sources
In progress:
- PuppetDB
To be written:
- Icinga2
- RackTables
- Cisco Prime
- VMware vCenter
- System Center Virtual Machine Manager
- Active Directory
- DNS:
 - PowerDNS
