# sovrin-agent

This is a reference implementation of a basic Sovrin Agent. A Sovrin Agent is
a persistent internet addressable endpoint dedicated to supporting the 
interactions one individual or organization. Sovrin Agents are not required to 
interact with others or with the Sovrin network. A Sovrin Agent could provide 
services for its owner, such as monitoring, notification, messaging, backups, 
and interacting with the Sovrin Distributed Identity Ledger.  

## Pre-requisite
- Python > 3.5

## Steps to install
- Clone this repository and switch to cloned repository directory
- `$ pip install -r requirements.txt`

## Steps to run api
- `$ python -m agent.scripts.startApiServer.py 0.0.0.0 8080`
- Run `$ pytest` to run all tests
