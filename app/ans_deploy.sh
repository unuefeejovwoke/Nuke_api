#!/bin/bash

cd ../ansible
ansible-playbook --private-key ~/Downloads/udacity.pem  -u ubuntu  server.yaml
cd -
