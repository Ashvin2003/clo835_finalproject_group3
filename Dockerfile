FROM ubuntu:20.04
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip \
    && apt-get install -y mysql-client \
    && apt-get install -y libjpeg-dev zlib1g-dev libpng-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /app/static/images
EXPOSE 81
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]