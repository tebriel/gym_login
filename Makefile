.PHONY: build push release

NOW=$(shell printf `cat TAG`)

all: date build push release

build:
	docker build -t cmoultrie/gym_login:${NOW} .
	docker tag cmoultrie/gym_login:${NOW} cmoultrie/gym_login:latest

run: build
	docker run --rm -it \
		-p 8080:80 \
		-e SHEET_ID \
		-e SHEET_FORM='Form Responses 1' \
		-v /Users/tebriel/.credentials:/data \
		cmoultrie/gym_login:latest

push:
	docker push cmoultrie/gym_login:${NOW}
	docker push cmoultrie/gym_login:latest

release:
	./scripts/release.sh ${NOW}

date:
	echo `date +%s` > TAG
