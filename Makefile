.PHONY: build push release

NOW=$(shell printf `cat TAG`)

all: date build push release

build:
	docker build -t cmoultrie/gym_login:${NOW} .
	docker tag cmoultrie/gym_login:${NOW} cmoultrie/gym_login:latest

run:
	docker run --rm -it \
		-p 8080:80 \
		-e SHEET_ID \
		-e SHEET_FORM='Form Responses 1' \
		-e DEVELOPMENT=True \
		-v /Users/tebriel/.credentials:/data \
		-v $(shell pwd)/gym_login:/usr/src/app/gym_login:ro \
		cmoultrie/gym_login:latest \
		pserve production.ini

push:
	docker push cmoultrie/gym_login:${NOW}
	docker push cmoultrie/gym_login:latest

release:
	./scripts/release.sh ${NOW}

date:
	echo `date +%s` > TAG
