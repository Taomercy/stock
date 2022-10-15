FROM taomercy/ubuntu-python3.7.4-nginx-django3:latest
WORKDIR /usr/src/app
COPY . .
RUN apt-get update
RUN python3 -m pip install --upgrade --force pip
RUN pip3 install setuptools==33.1.1
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD python3 main.py
