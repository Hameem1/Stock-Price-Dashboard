FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev
RUN apt-get install -y language-pack-de
RUN cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN  mkdir /Stock_Price_Dashboard
WORKDIR /Stock_Price_Dashboard
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]