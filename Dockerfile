FROM python:3.5-onbuild

EXPOSE 80

VOLUME ["/data"]

ENV SHEET_ID= \
    SHEET_FORM= \
    DEVELOPMENT=False

RUN pip install -e .

CMD pserve production.ini
