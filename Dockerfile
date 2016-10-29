FROM python:3.5-onbuild

EXPOSE 80

VOLUME ["/data"]

ENV LOGIN_SHEET_ID= \
    USERS_SHEET_ID= \
    DEVELOPMENT=False

RUN pip install -e .

CMD pserve production.ini
