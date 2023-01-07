FROM python:3.8
RUN pip install socket
RUN pip install re
WORKDIR /http_service
COPY http_service.py /http_service/http_test
CMD ["python3","http_service"]