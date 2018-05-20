FROM 172.18.248.180:5000/yg-cleaner-base:v1

ADD ./src /src
WORKDIR /src

EXPOSE 23052

RUN mkdir -p ~/.pip/
RUN echo '[global]' >> ~/.pip/pip.conf
RUN echo 'trusted-host =  mirrors.aliyun.com' >> ~/.pip/pip.conf
RUN echo 'index-url = http://mirrors.aliyun.com/pypi/simple' >> ~/.pip/pip.conf

RUN ["pip3", "install", "redis"]
RUN ["pip3", "install", "happybase"]
RUN ["pip3", "install", "requests"]
RUN ["pip3", "install", "flask"]
RUN ["pip3", "install", "tornado"]
RUN ["pip3", "install", "bs4"]

CMD ["python3.5", "commander.py"]
