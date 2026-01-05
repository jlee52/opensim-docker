# Overview
This repository provides a docker setup to run OpenSim on cross-platform (e.g, wsl, mac, linux). This contains docker compose and baseline python script to run OpenSim processing pipeline: scale, inverse kinematics, etc. For details of OpenSim, see the official OpenSim documentations [OpenSim Documentation](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/overview).


We provide docker container including
- Ubuntu 22.04
- OpenSim 4.5
- OpenSim Python binding

# Pre-requisite
## Install Docker
- [Docker Engine](https://docs.docker.com/engine/install/)

## Install Docker Compose
- [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Linux](https://docs.docker.com/compose/install/linux/#install-using-the-repository)

# Installation
1) Clone the repository
    ```
    git clone https://github.com/jlee52/opensim-docker.git
    ```

2) Run docker compose up
    
    The following command builds containers based on `Dockerfile` and `docker-compose.yaml`. After completion of building, the container can be started running in backgroud by using `docker compose up -d` without `--build` argument. Running docker can be checked by `docker ps`.
    ```
    cd {your_ws}/opensim-docker
    docker compose up --build -d  
    ```
    Note. linux needs `sudo` to run docker. To manage docker as non-root user, refer [linux post-installation guide](https://docs.docker.com/engine/install/linux-postinstall/).

# Execution
To open an interactive terminal shell inside a running Docker container, 
```
docker exec -it opensim_container /bin/bash
```
In the interctie terminal shell, run OpenSim Python script
```
python3 runScale.py
```
