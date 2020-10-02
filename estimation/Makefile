IMAGE_NAME = stockestimation
CONTAINER_NAME = StockEstimation

VOLUME_OPTS = --volume $(abspath .):/Python

all:
.PHONY += all

build: Dockerfile
	docker build --rm --tag $(IMAGE_NAME) .
.PHONY += build

delete:
	docker rmi $(IMAGE_NAME)
.PHONY += delete

start:
	docker run --name $(CONTAINER_NAME) --detach --restart "always" --publish-all $(VOLUME_OPTS) $(IMAGE_NAME)
.PHONY += start

test:
	docker run --name $(CONTAINER_NAME) --rm --interactive --tty --publish-all $(VOLUME_OPTS) $(IMAGE_NAME) python3 /test.py

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
