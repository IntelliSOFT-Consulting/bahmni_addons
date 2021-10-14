## Copy files to server

`cd /opt/bahmni-erp/bahmni-addons`

`git clone https://github.com/IntelliSOFT-Consulting/bahmni_addons.git bahmni_mtiba`

`chown odoo.odoo -Rf bahmni_mtiba`

Restart the odoo service 
`sudo service odoo restart` 

## Install the module

log in to the odoo instance

Turn developer mode on

Go to addons and search for `mtiba`

Once you find it, install it

## Configure the module

Go to `Settings --> Parameters --> System Parameters`

Check tha `mtiba-base.url` parameter has been setup properly

## Setup m-tiba credentials

Go to `Accounting --> Settings`

Set `Mtiba username (GET)` and `Mtiba password (GET)` -- Use OpenMRS login credentials

Set `Mtiba username` and `Mtiba password`

Set `Payment terms` to "Mtiba". Create one if it doesn't exist

Apply

