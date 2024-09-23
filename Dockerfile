FROM amazonlinux

WORKDIR /home/kinesis
COPY . .

RUN yum install -y aws-kinesis-agent
RUN yum install -y vi
RUN yum install -y pip
RUN pip install -r requirements.txt 
RUN yum install sudo -y
RUN yum install initscripts -y   # its to enable service cmd

ENV LOG_DIR=/home/kinesis/logs
ENV LOG_FILE=/home/kinesis/logs/users_activity.log

CMD ["python3","generate_logs.py"]

RUN sudo service aws-kinesis-agent start