RANDOM := $(shell bash -c 'echo $$RANDOM')
DATE := $(shell date "+%y%m%d")
IMAGE_NAME = stockcrawling:$(DATE)

DETACH_OPTS = --detach --restart "always" --publish-all 

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

start: Stock Name Index KRX
.PHONY += start

stop:
	docker ps | grep Stock && docker stop Stock_$(DATE) && dockre rm Stock_$(DATE)
.PHONY += stop

Stock: stock.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<

Name: name.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<

Index: index.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<

KRX: KRX.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<
