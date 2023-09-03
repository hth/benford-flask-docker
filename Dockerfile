FROM python:3.11
LABEL maintainer="hth"

COPY . /app
WORKDIR /app

RUN mkdir -p /tmp/upload
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["src/appInitialize.py"]
