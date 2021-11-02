# my_deployer CLI made with Python

## Description
The main goal of this project is to create a handy, automated deployment tool based on SSH.
To put it simply, it will have to deploy Docker containers on a remote host, and therefore configure it appropriately beforehand.

Your project will consist of a script providing a CLI with multiple subcommands to manage the services on the remote host:

- `config`: configure the remote host
- `build`: build Docker images for the services
- `deploy`: deploy the services
- `healthcheck`: ensure the services are running properly

## Installation
```bash
pip install .
```
## Available Commands
```bash
# Install docker on the remote server
python3 my_deployer config ssh://tinky@localhost:2222

# Build images on the remote server
python3 my_deployer build ssh://tinky@localhost:2222 checker --tag latest
python3 my_deployer build ssh://tinky@localhost:2222 system --tag latest

# Deploy on the remote server
python3 my_deployer deploy ssh://tinky@localhost:2222 checker --tag latest
python3 my_deployer deploy ssh://tinky@localhost:2222 system --tag latest

# Check the health of your containers
python3 my_deployer healthcheck ssh://tinky@localhost:2222 checker
python3 my_deployer healthcheck ssh://tinky@localhost:2222 system

# Check the health of all your containers
python3 my_deployer healthcheck ssh://tinky@localhost:2222
```