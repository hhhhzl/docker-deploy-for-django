FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /DESP

EXPOSE 8000

# python dependencies
RUN pip install \
    Django==3.2.4 \
    django-filter==2.4.0 \
    djangorestframework==3.12.4 \
    djangorestframework-bulk==0.2.1 \
    django-cors-headers==3.8.0 \
    drf-yasg==1.20.0 \
    PyMySQL==1.0.2 \
    cryptography==3.4.5

COPY . /DESP
