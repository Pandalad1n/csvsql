
.PHONY: start
start:
	docker-compose up -d

.PHONY: stop
stop:
	docker-compose down

.PHONY: test
test:
	docker-compose run app python app/test.py