FROM 172.18.248.180:5000/yg-cleaner-base:v1

ADD ./src /src
WORKDIR /src

EXPOSE 23051

RUN mkdir -p ~/.pip/
RUN echo '[global]' >> ~/.pip/pip.conf
RUN echo 'trusted-host =  mirrors.aliyun.com' >> ~/.pip/pip.conf
RUN echo 'index-url = http://mirrors.aliyun.com/pypi/simple' >> ~/.pip/pip.conf

CMD ["python3.5", "commander.py"]
