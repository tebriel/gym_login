.PHONY: build push release

all: build test push release

build:
	docker build -t cmoultrie/gym_login:latest .

push:
	docker push cmoultrie/gym_login:latest .

test: build
	docker run --rm cmoultrie/gym_login:latest py.test

release:
	./scripts/release.sh
