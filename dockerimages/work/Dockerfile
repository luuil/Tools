# Ref. to https://docs.docker.com/get-started/part2/#define-a-container-with-dockerfile

# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Clears out the local repository of retrieved package files.
# And then, downloads the package lists from the repositories and "updates" them to get
# information on the newest versions of packages and their dependencies.
RUN apt-get clean && apt-get -y update

# Install nano, openssh, keychain
# RUN apt-get install -y openssh-server
RUN apt-get install -y openssh-client
RUN apt-get install -y keychain
RUN apt-get install -y nano

# Set the working directory to /root
WORKDIR /root

# ADD files to /root
ADD .ssh .ssh
COPY .bash_profile .

# Make sure the files are not readable for other users/groups.
RUN chmod 600 .ssh/Identity .ssh/Identity.pub

# append keychain support to bashrc
# sed -i '$a <content>' file: means append contents to file in-place.
RUN sed -i '$a \n# ssh keychain\neval `keychain --eval ~/.ssh/Identity`' .bashrc

# ADD ssh-dss, forward support ro openssh-client, because of the `Identity` is type of ssh-dss.
RUN sed -i '$a PubkeyAcceptedKeyTypes=+ssh-dss' /etc/ssh/ssh_config
RUN sed -i '$a ForwardAgent yes' /etc/ssh/ssh_config

# ADD ssh-dss support ro openssh-server
# RUN sed -i '$a PubkeyAcceptedKeyTypes=+ssh-dss' /etc/ssh/sshd_config
