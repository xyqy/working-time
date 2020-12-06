FROM python:3.6

MAINTAINER "Qi Yayu<65644853@qq.com>"

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
EXPOSE 5010
ENTRYPOINT ["python"]
CMD ["app.py"]