FROM python:3
WORKDIR /usr/src/app

COPY build .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD python main.py