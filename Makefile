.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	docker-compose up

.PHONY: stop
stop:
	docker-compose down

.PHONY: test
test:
	docker-compose run app python app/test/run.py
