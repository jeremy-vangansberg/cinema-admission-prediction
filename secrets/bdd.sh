#!/bin/bash
RESOURCE_GROUP=RG_VANGANSBERG
ACI_PERS_STORAGE_ACCOUNT_NAME=storagejv1
ACI_PERS_LOCATION=francecentral
ACI_PERS_SHARE_NAME=cinemabdd
STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $ACI_PERS_STORAGE_ACCOUNT_NAME --query "[0].value" --output tsv)



az container create \
  --resource-group $RESOURCE_GROUP \
  --name postgres \
  --image postgres\
  --dns-name-label postgrescine \
  --ports 5432 \
  --ip-address public \
  --cpu 1 \
  --memory 8 \
  --environment-variables 'POSTGRES_USER=user' 'POSTGRES_DB=mydb' 'POSTGRES_PASSWORD=mysecretpassword' \
  --azure-file-volume-account-name $ACI_PERS_STORAGE_ACCOUNT_NAME \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-share-name $ACI_PERS_SHARE_NAME \
  --azure-file-volume-mount-path /var/lib/postgresql/data