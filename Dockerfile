FROM python:3.6-stretch

RUN mkdir -p /src && \
    pip install --no-cache-dir falcon

COPY apimock.py /src/

WORKDIR /src
ENV PYTHONPATH /src

EXPOSE 8080

CMD ["python", "apimock.py"]