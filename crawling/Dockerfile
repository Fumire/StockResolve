FROM python:3.8.5
LABEL maintainer="230@fumire.moe"

ADD requirements.txt /
RUN pip3 install --no-cache-dir --requirement /requirements.txt

ADD *.py /
ADD password*.txt /
Add data.xls /

EXPOSE 3306
RUN echo "nameserver 1.1.1.1" >> /etc/resolv.conf

CMD ["/bin/bash"]
