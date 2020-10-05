IMAGE_NAME = stockestimation

all:
.PHONY += all

build: Dockerfile
	docker build --rm --tag $(IMAGE_NAME) .
.PHONY += build

delete:
	docker rmi $(IMAGE_NAME)
.PHONY += delete

start: Estimation Result
.PHONY += start

interactive:
	docker run --name Estimation --rm --interactive --tty --publish-all $(IMAGE_NAME) /bin/bash || true

stop:
	docker ps | grep Estimation && docker stop Estimation && docker rm Estimation || true
	docker ps | grep Result && docker stop Result && docker rm Result || true

Estimation:
	docker ps | grep $@ || docker run --name $@ --detach --restart "always" --publish-all $(IMAGE_NAME) python3 /estimation.py

Result:
	docker ps | grep $@ || docker run --name $@ --detach --restart "always" --publish-all $(IMAGE_NAME) python3 /result.py
