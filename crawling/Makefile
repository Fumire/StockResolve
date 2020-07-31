IMAGE_NAME = stockestimation

all:
.PHONY += all

build: Dockerfile
	docker build --rm --tag $(IMAGE_NAME) .
.PHONY += build

delete:
	docker rmi $(IMAGE_NAME)
.PHONY += delete

test:
	docker run --name Test --rm --interactive --tty --publish-all $(IMAGE_NAME)
.PHONY += test
