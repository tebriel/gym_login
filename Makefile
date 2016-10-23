.PHONY: build push release

NOW=$(shell printf `cat TAG`)

all: date build push release

build:
	docker build -t cmoultrie/gym_login:${NOW} .

push:
	docker push cmoultrie/gym_login:${NOW}

release:
	./scripts/release.sh ${NOW}

date:
	echo `date +%s` > TAG
