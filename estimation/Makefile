IMAGE_NAME = stockestimation
CONTAINER_NAME = StockEstimation

all:
.PHONY += all

build: Dockerfile
	docker build --rm --tag $(IMAGE_NAME) .
.PHONY += build

delete:
	docker rmi $(IMAGE_NAME)
.PHONY += delete

start:
	docker run --name $(CONTAINER_NAME) --detach --restart "always"  --publish-all $(IMAGE_NAME)
.PHONY += start

test:
	docker run --name $(CONTAINER_NAME) --rm --interactive --tty --publish-all $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
