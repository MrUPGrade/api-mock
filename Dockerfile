FROM python:3.6-stretch

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

VOLUME /mock/
ENV PYTHONPATH /src

EXPOSE 8080

ADD apimock /src/apimock

CMD ["python", "-m", "apimock"]