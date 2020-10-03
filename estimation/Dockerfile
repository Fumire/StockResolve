FROM python:3.8.5
LABEL maintainer="230@fumire.moe"

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

ADD requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir --requirement /requirements.txt

ADD *.py /
ADD password*.txt /

EXPOSE 3306

CMD ["/bin/bash"]
