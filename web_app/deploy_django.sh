#!/bin/bash
RESOURCE_GROUP=RG_VANGANSBERG

az container create \
  --resource-group $RESOURCE_GROUP \
  --name django-cinema \
  --image j30v/django-cinema \
  --dns-name-label cinema-pred \
  --ports 80 \
  --memory 4\
  --ip-address public \
