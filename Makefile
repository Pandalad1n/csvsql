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

.PHONY: dbshell
dbshell:
	docker-compose run app psql

.PHONY: openapi
openapi:
	docker pull swaggerapi/swagger-ui
	docker run \
	    --network="host" \
	    -e URL=http://localhost/swagger.yaml \
	    swaggerapi/swagger-ui
