FROM python:3.10
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y cmake
RUN pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r requirements.txt
#ENV MY_ENV_VAR=my_value
ENV PYTHONPATH=$PYTHONPATH:/app
