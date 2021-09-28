# zabbix-users-objects-exporter

### this script export all users objects like hostgroup, mediatypes, usergroups and users itself from a given zabbix server to a receiver zabbix server in order to preserve all usergroup permissions in the objects shifting


# caveats
### due to zabbix api limitations it's not possible export through the api users passwords, that mean that the user copy from a server to another works only if the usergroup have ldap fronten access enabled, if the usergroup already exist on the receiver server and do not have ldap frontend access enabled the user will not be copy but, if the usergroup do not exist on the receiver server the script will provide by itself to ricreate the usergroup with ldap frontend access already enabled


# deps and configuration
### the only python module required to run the script is pyzabbix, you can install it with pip:
> pip install pyzabbix
### to configure yours input and output zbx servers, just open the script and edit the required params in the configuration section   
