FROM python:3.8.5
LABEL maintainer="230@fumire.moe"

ADD requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir --requirement /requirements.txt

ADD estimation.py /
ADD password*.txt /

EXPOSE 3306

ENTRYPOINT ["python3", "/estimation.py"]
