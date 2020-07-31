IMAGE_NAME = stockcrawling

all:
.PHONY += all

build: Dockerfile
	docker build --rm --tag $(IMAGE_NAME) .
.PHONY += build

delete:
	docker rmi $(IMAGE_NAME)
.PHONY += delete

test: test.py
	docker run --name Test --rm --tty --publish-all $(IMAGE_NAME) python3 /test.py
.PHONY += test

interactive:
	docker run --name Test --rm --interactive --tty --publish-all $(IMAGE_NAME)
.PHONY += interactive
