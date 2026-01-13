# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies
# Added 'python3-dev' (headers required for compiling bindings) and 'numpy' (required for wrapping)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    sudo \
    wget \
    unzip \
    bison \
    flex \
    python3 \
    python3-dev \
    python3-pip \
    swig \
    liblapack-dev \
    libopenblas-dev \
    freeglut3-dev \
    libxi-dev \
    libxmu-dev \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8

# Create Directory
WORKDIR /root/repos

# Clone OpenSim Core
RUN git clone https://github.com/opensim-org/opensim-core
# RUN git clone https://github.com/MIT-Motor-Control/mocap-tools.git

# Before the OpenSim build step, install the JDK
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME so CMake can find the JNI headers automatically
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install OpenSim and Python bindings
RUN opensim-core/scripts/build/opensim-core-linux-build-script.sh -j 2

WORKDIR /root/opensim-core/sdk/Python/
RUN python3 -m pip install .
RUN pip3 install numpy==1.26.4

# Set environment variables for OpenSim
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/opensim-core/sdk/lib
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/opensim-core/sdk/Simbody/lib

# CHANGE: Keep the container running indefinitely so you can access it
CMD ["tail", "-f", "/dev/null"]
