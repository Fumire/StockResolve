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
	docker ps | grep Stock && docker stop Stock_$(DATE) && docker rm Stock_$(DATE)
	docker ps | grep Name && docker stop Name_$(DATE) && docker rm Name_$(DATE)
	docker ps | grep Index && docker stop Index_$(DATE) && docker rm Index_$(DATE)
	docker ps | grep KRX && docker stop KRX_$(DATE) && docker rm KRX_$(DATE)
.PHONY += stop

Stock: stock.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<

Name: name.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<

Index: index.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<

KRX: KRX.py
	docker ps | grep $@ || docker run --name $@_$(DATE) $(DETACH_OPTS) $(IMAGE_NAME) python3 /$<
