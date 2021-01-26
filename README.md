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

GOt settings --> Parametes --> System Parameters

Check tha mtiba-base.url parameter has been setup proprtly

## Setup m-tiba credentials

Go to accounting --> Settings

Set Mtiba username and password

Set payment term to "Mtiba". Create one if it doesn't exist

Apply

