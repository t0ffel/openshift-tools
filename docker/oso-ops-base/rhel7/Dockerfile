#     ___ ___ _  _ ___ ___    _ _____ ___ ___         
#    / __| __| \| | __| _ \  /_\_   _| __|   \        
#   | (_ | _|| .` | _||   / / _ \| | | _|| |) |       
#    \___|___|_|\_|___|_|_\/_/_\_\_|_|___|___/_ _____ 
#   |   \ / _ \  | \| |/ _ \_   _| | __|   \_ _|_   _|
#   | |) | (_) | | .` | (_) || |   | _|| |) | |  | |  
#   |___/ \___/  |_|\_|\___/ |_|   |___|___/___| |_|  
# 

FROM rhel7:latest

# Pause indefinitely if asked to do so.
RUN test "$OO_PAUSE_ON_BUILD" = "true" && while true ; do sleep 10 ; done || :

# get rid of subscript manager (we use our own mirrors)
RUN touch /var/run/rhsm ; rpm -evh subscription-manager

# setup yum repos
ADD setup-yum.sh /usr/local/bin/setup-yum.sh
RUN /usr/local/bin/setup-yum.sh

# creature comforts (make it feel like a normal linux environment)
ENV LANG en_US.UTF-8
ENV CONTAINER docker
ENV USER root
ENV HOME /root
ENV TERM xterm
WORKDIR /root
ADD root/bashrc /root/.bashrc
ADD root/pdbrc /root/.pdbrc

# Make working in Python nice
ADD root/pythonrc /root/.pythonrc
ENV PYTHONSTARTUP=/root/.pythonrc

# setup epel repo
RUN rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

RUN yum clean metadata && \
    yum -y update && \
    yum -y install iputils cronie ansible1.9 vim procps less ack tar psmisc python-scandir && \
    yum clean all

# Setup locales.  It comes broken (probably a size issue) by default in the docker image.
RUN yum -y reinstall glibc-common &&  \
    yum clean all  && \
    mv -f /usr/lib/locale/locale-archive /usr/lib/locale/locale-archive.tmpl  && \
    /usr/sbin/build-locale-archive

# Setup Cron
ADD pamd.crond /etc/pam.d/crond

# Setup Ansible
ADD ansible.cfg /etc/ansible/ansible.cfg
RUN echo -e '[local]\nlocalhost       ansible_connection=local\n' > /etc/ansible/hosts

# Make the container work more consistently in and out of openshift
# BE CAREFUL!!! If you change these, you may bloat the image! Use 'docker history' to see the size!
RUN chmod -R g+rwX /root/
