FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu16.04
COPY sources.list /etc/apt/sources.list
RUN rm -rf /etc/apt/sources.list.d/cuda*
RUN rm -rf /etc/apt/sources.list.d/nvidia*

RUN rm -rf /var/lib/apt/lists/* &&\
    apt-get clean &&\
    apt-get update  &&\
    apt-get install -y --no-install-recommends \
        wget curl ca-certificates unzip autoconf libtool automake tzdata \
        vim git build-essential cmake pkg-config tree software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y imagemagick
RUN rm /etc/ImageMagick-6/policy.xml
COPY policy.xml /etc/ImageMagick-6/policy.xml
RUN apt-get install -y openssh-server
RUN apt-get install -y libsm6
RUN apt-get install -y libxrender1


ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
ENV PYTHONIOENCODING=utf-8

RUN mkdir /root/.pip
COPY pip.conf /root/.pip/pip.conf

RUN echo 'Asia/Shanghai' >/etc/timezone && rm -rf /etc/localtime && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
WORKDIR /root/


COPY Miniconda3-4.7.12.1-Linux-x86_64.sh /root/
RUN /bin/bash /root/Miniconda3-4.7.12.1-Linux-x86_64.sh -b -p /root/miniconda3 && rm /root/Miniconda3-4.7.12.1-Linux-x86_64.sh
RUN echo '\n\
__conda_setup="$('/root/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"\n\
if [ $? -eq 0 ]; then\n\
    eval "$__conda_setup"\n\
else\n\
    if [ -f "/root/miniconda3/etc/profile.d/conda.sh" ]; then\n\
        . "/root/miniconda3/etc/profile.d/conda.sh"\n\
    else\n\
        export PATH="/root/miniconda3/bin:$PATH"\n\
    fi\n\
fi\n\
unset __conda_setup\n' >> ~/.bashrc && /bin/bash -c 'source  ~/.bashrc'
RUN echo "\
channels:\n\
   - defaults\n\
show_channel_urls: true\n\
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda\n\
default_channels:\n\
   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main\n\
   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free\n\
   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r\n\
   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro\n\
   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2\n\
custom_channels:\n\
   conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
   msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
   bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
   menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
   pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n\
   simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud\n" > ~/.condarc
RUN ln -sf /root/miniconda3/bin/conda /bin/conda
RUN conda create -n torch_new python=3.8.5 -y
RUN ln -sf /root/miniconda3/envs/torch_new/bin/pip /bin/pip
RUN ln -sf /root/miniconda3/envs/torch_new/bin/python /bin/python
RUN echo '\n\
conda activate torch_new\n'  >> ~/.bashrc && /bin/bash -c 'source  ~/.bashrc'

COPY torch-1.7.1+cu101-cp38-cp38-linux_x86_64.whl /root/
RUN pip install /root/torch-1.7.1+cu101-cp38-cp38-linux_x86_64.whl && rm /root/torch-1.7.1+cu101-cp38-cp38-linux_x86_64.whl
RUN pip install torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
COPY requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt
RUN pip list &&python -V


# FROM testcuda:v1.2
# FROM cuda10.1-cudnn7-py38:1.0.0
#FROM cuda10.1-cudnn7-py36-torch1.7:1.0.0
# RUN apt-get update && apt-get install -y python3-wand libsm-dev libxrender-dev python3.6-dev
#RUN apt-get install -y openssh-server
# RUN /etc/init.d/ssh start
#COPY requirements.txt /root/requirements.txt
# COPY tensorflow /root/tensorflow
# COPY torch /root/torch
# COPY numpy /root/numpy
# COPY h5py /root/h5py

# RUN pip install /root/numpy/numpy-1.19.4-cp36-cp36m-manylinux2010_x86_64.whl
# RUN pip install /root/h5py/h5py-3.1.0-cp36-cp36m-manylinux1_x86_64.whl
# RUN pip install /root/tensorflow/tensorflow_gpu-1.15.0-cp36-cp36m-manylinux2010_x86_64.whl
# RUN pip install /root/torch/torch-1.2.0-cp36-cp36m-manylinux1_x86_64.whl
# RUN pip install /root/torch/torchvision-0.4.0-cp36-cp36m-manylinux1_x86_64.whl
# RUN pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
# RUN pip install -r /root/requirements.txt

# COPY server /root/server

# COPY server/policy.xml /etc/ImageMagick-6/

# VOLUME ["/model"]
# VOLUME ["/conf"]

#WORKDIR /root/server
# RUN mkdir /volume
# RUN rm -rf /root/tensorflow
# RUN rm -rf /root/torch
# RUN rm -rf /root/numpy
# RUN rm -rf /root/h5py
# CMD ["python","server.py","ProdEnv"]




FROM cuda10.1-cudnn7-conda-torch17:1.0.0

RUN mkdir -p /root/.cache/torch/hub/checkpoints/
COPY OCR_deploy /root/
COPY resnet50-19c8e357.pth /root/.cache/torch/hub/checkpoints/
COPY volume /

RUN pip install configobj==5.0.6
RUN pip install thrift==0.13.0

 VOLUME ["/model"]
 VOLUME ["/conf"]

WORKDIR /root/OCR_deploy

CMD ["python","server.py","ProdEnv"]
