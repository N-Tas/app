# 
FROM python:3.7.3

# 
WORKDIR /code

# 
COPY . .

# 
RUN apt-get install gcc

ADD odbcinst.ini /etc/odbcinst.ini
RUN apt-get update
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc-bin -y
RUN apt-get clean -y

RUN pip3 install -r requirements.txt

# 
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]