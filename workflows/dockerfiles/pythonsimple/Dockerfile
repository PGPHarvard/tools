FROM arvados/jobs:latest
USER root

# Installing apt-utils
RUN apt-get install -y --no-install-recommends apt-utils

# installing zlib1g-dec
RUN apt-get install zlib1g-dev -y

# install bzip
RUN apt-get install bzip2 -y

# install unzip
RUN apt-get install unzip -y

# install gzip
RUN apt-get install gzip -y

# System packages 
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

# Python packages from conda
RUN conda install -c conda-forge -c bioconda gsort htslib

# Clean up
RUN apt-get clean

