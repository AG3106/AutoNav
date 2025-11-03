# ============================================================
# Grounded-Segment-Anything Dockerfile (stable build)
# - Torch 2.1.0 + CUDA 11.8
# - segment-anything official repo
# - supervision 0.17.1
# ============================================================

FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# ---------------------------
# Install Python, pip, and PyTorch
# ---------------------------
RUN apt-get update && apt-get install -y python3-pip python3-dev && \
    pip install --upgrade pip
RUN pip install torch==2.0.1 torchvision==0.15.2 transformers==4.42.0
# ---------------------------
# Env setup
# ---------------------------
ARG USE_CUDA=1
ARG TORCH_ARCH="8.6"

ENV AM_I_DOCKER=True
ENV BUILD_WITH_CUDA="${USE_CUDA}"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_ARCH}"
ENV CUDA_HOME=/usr/local/cuda-11.8
ENV TZ=Asia/Kolkata
ENV GSA_PATH=/home/appuser/Grounded-Segment-Anything
# Set the env variables as follows (change the paths accordingly)
ENV LLAVA_PYTHON_PATH=/home/appuser/LLaVA/llava
ENV LLAVA_CKPT_PATH=/path/to/LLaVA-7B-v0
ENV CG_FOLDER=/home/appuser/concept-graphs/
# ---------------------------
# System packages
# ---------------------------
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git wget ffmpeg libsm6 libxext6 nano vim x11-apps tzdata gnupg2 ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ---------------------------
# Workspace
# ---------------------------
RUN mkdir -p $GSA_PATH
COPY ./Grounded-Segment-Anything $GSA_PATH
WORKDIR $GSA_PATH

# ---------------------------
# Python setup
# ---------------------------
RUN python3 -m pip install --upgrade pip wheel setuptools

# Core dependencies
RUN pip install \
    opencv-python==4.7.0.72 \
    pycocotools==2.0.6 \
    matplotlib==3.5.3 \
    onnxruntime==1.14.1 \
    onnx==1.13.1 \
    ipykernel==6.16.2 \
    scipy gradio openai \
    tyro wandb h5py hydra-core==1.3.2 distinctipy ultralytics

# ---------------------------
# segment-anything (official)
# ---------------------------
RUN pip install git+https://github.com/facebookresearch/segment-anything.git

# ---------------------------
# GroundingDINO (local editable)
# ---------------------------
RUN pip install --no-build-isolation -e GroundingDINO

# ---------------------------
# supervision (compatible version)
# ---------------------------
RUN pip install supervision==0.18.0

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     g++-11 gcc-11
    
# ENV CXX=g++-11 CC=gcc-11

# ---------------------------
# Faiss + PyTorch3D
# ---------------------------
RUN pip install faiss-cpu==1.7.4
RUN pip install "git+https://github.com/facebookresearch/pytorch3d.git@v0.7.4"

# ---------------------------
# chamferdist + gradslam
# ---------------------------
WORKDIR /home/appuser
RUN git clone https://github.com/krrish94/chamferdist.git && pip install chamferdist
RUN git clone https://github.com/gradslam/gradslam.git && cd gradslam && git checkout conceptfusion && pip install .

# ---------------------------
# LLaVA
# ---------------------------
RUN git clone https://github.com/haotian-liu/LLaVA.git && \
    cd LLaVA && git checkout 8fc54a09a6be74b2abd913c468fb3d42ae826194 && pip install -e .

# ---------------------------
# concept-graphs
# ---------------------------
RUN git clone https://github.com/concept-graphs/concept-graphs.git && \
    pip install -e concept-graphs

# ---------------------------
# Final workspace
# ---------------------------
RUN pip install timm==0.4.12 open_clip_torch fairscale==0.4.4 pycocoevalcap
RUN pip install git+https://github.com/openai/CLIP.git
WORKDIR /home/appuser

# ---------------------------
# ROS Noetic + Jackal Simulator installation
# ---------------------------
RUN apt-get update && apt-get install -y locales curl gnupg2 lsb-release && \
    locale-gen en_US en_US.UTF-8 && \
    echo "source /opt/ros/noetic/setup.bash" >> /etc/bash.bashrc && \
    sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - && \
    apt-get update && \
    apt-get install -y ros-noetic-desktop-full python3-rosdep python3-rosinstall python3-rosinstall-generator \
                       python3-wstool build-essential python3-catkin-tools && \
    rm -rf /var/lib/apt/lists/*

# Initialize rosdep
RUN rosdep init && rosdep update

# ---------------------------
# Jackal Simulator (Gazebo)
# ---------------------------
RUN sh -c 'echo "deb http://packages.clearpathrobotics.com/stable/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/clearpath-latest.list' && \
    curl -s https://packages.clearpathrobotics.com/public.key | apt-key add - && \
    apt-get update && \
    apt-get install -y ros-noetic-jackal-simulator ros-noetic-jackal-desktop ros-noetic-jackal-gazebo \
                       ros-noetic-jackal-navigation ros-noetic-jackal-control && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# Source environment
# ---------------------------
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc


RUN git clone https://github.com/sachaMorin/concept_graphs_jackal.git
