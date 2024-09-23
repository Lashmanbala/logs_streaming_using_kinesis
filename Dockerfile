FROM amazonlinux

WORKDIR /home/kinesis
COPY . .

RUN yum install -y aws-kinesis-agent
COPY agent.json /etc/aws-kinesis/agent.json

RUN yum install -y vi
RUN yum install -y pip
RUN pip install -r requirements.txt 
RUN yum install sudo -y
RUN yum install initscripts -y   # its to enable service cmd
RUN sudo service aws-kinesis-agent start

ENV LOG_DIR=/home/kinesis/logs
ENV LOG_FILE=/home/kinesis/logs/users_activity.log
