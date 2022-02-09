<!-- ABOUT THE PROJECT -->
## About The Project
`jobberwocky` app is a service that works as a store for job opportunities where
companies can share open positions

<!-- GETTING STARTED -->
## Getting Started
***
You can use docker and/or Makefile to run the project.
### Prerequisites
In order to run the project you will need the following:
* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/)
* [GNU Make](https://www.gnu.org/software/make/)

## How to
***
1. Rewrite .env.example to your own .env with the webpage you wanna obtain the
images from
2. Execute ```make up``` to bring all the services up and running
3. Navigate [local-jobberwocky](http://localhost:8000/docs#/jobs) to check docs
and try the API
4. If you want to pre-populate the DB you can use ```make dummy_data```

## Run test suite
***
Execute ```make test``` to run all the tests

## Additional tools
Execute ```make psql``` to have psql terminal to postgres
Execute ```make bash``` to have shell into app service.
Execute ```make dummy_data``` to populate DB with random Data to test out the app