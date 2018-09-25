# Ref. to https://docs.docker.com/get-started/part2/#define-a-container-with-dockerfile

# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Set the working directory to /root
WORKDIR /root


# =========================Service SUPPORT===================================

# Clears out the local repository of retrieved package files.
# And then, downloads the package lists from the repositories and "updates" them to get
# information on the newest versions of packages and their dependencies.
RUN apt-get clean && apt-get -y update

# Install nano, openssh, keychain, sudo, rsync, dos2unix
# RUN apt-get install -y openssh-server
RUN apt-get install -y openssh-client
RUN apt-get install -y keychain
RUN apt-get install -y nano
RUN apt-get install -y sudo
RUN apt-get install -y rsync
RUN apt-get install -y dos2unix

RUN rm -rf /var/lib/apt/lists/*


# =========================SSH SUPPORT===================================

# ADD files to /root
ADD .ssh .ssh
# COPY .bash_profile .

# Make sure the files are not readable for other users/groups.
RUN chmod 600 .ssh/Identity .ssh/Identity.pub

# append keychain support to bashrc
# sed -i '$a <content>' file: means append contents to file in-place.
RUN sed -i '$a # ssh keychain\neval `keychain --eval ~/.ssh/Identity`' .bashrc

# ADD ssh-dss, forward support ro openssh-client, because of the `Identity` is type of ssh-dss.
RUN sed -i '$a PubkeyAcceptedKeyTypes=+ssh-dss' /etc/ssh/ssh_config
RUN sed -i '$a ForwardAgent yes' /etc/ssh/ssh_config

# ADD ssh-dss support ro openssh-server
# RUN sed -i '$a PubkeyAcceptedKeyTypes=+ssh-dss' /etc/ssh/sshd_config

# Generate KEY
RUN ssh-keygen -q -t rsa -N '' -C 'for work login' -f ~/.ssh/id_rsa

# Copy to REMOTE
# ssh-copy-id -f -i ~/.ssh/id_rsa.pub <remote>


# =========================ALIAS SUPPORT===================================

ADD .sh .sh
RUN sed -i '$a # my alias\nsource ~/.sh/.bash_aliases' .bashrc