.PHONY: build test run clean

build:
	docker-compose -f docker/docker-compose.yml build

test:
	docker-compose -f docker/docker-compose.yml run --rm test

run:
	docker-compose -f docker/docker-compose.yml up

clean:
	docker-compose -f docker/docker-compose.yml down -v 