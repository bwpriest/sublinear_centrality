FROM ubuntu:trusty

#
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  rm -rf /var/lib/apt/lists/* && \
  curl -L -O https://github.com/xdata-skylark/libskylark/releases/download/v0.20/install.sh

# Add files.
ADD . /home

# Set environment variables.
ENV HOME /home

# Define working directory.
WORKDIR /home

# Move and install script to home directory
RUN mv /install.sh ./install.sh && \
	sudo bash install.sh -b -p ${HOME}/libskylark && \
	export PATH=${HOME}/libskylark/bin:${PATH}

RUN cp .bashrc /root/.bashrc


# Define default command.
CMD ["bash"]