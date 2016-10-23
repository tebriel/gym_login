.PHONY: build push release

build:
	docker build -t cmoultrie/gym_login:latest .

push:
	docker push cmoultrie/gym_login:latest .

release:
	./scripts/release.sh
