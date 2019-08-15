
#Table from csv or xlsx 
Microservice that accepts csv or xlsx file and creates table in DB.
Automatically determines column types.

To build project run `make build`.

To run all tests run `make test`.

To start microservice run `make start`. it will listen on port 80.

To stop microservice run `make stop`.


For local development you can use `make dbshell` to access database 
and `make openapi` to run openapi-UI server.

Openapi spec can be accessed at `/swagger.yaml` endpoint.