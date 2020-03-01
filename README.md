# Have I _NOT_ Been Owned

Perhaps the only API where you want to receive 404s from.

# Running

## Setup

1. Ensure you have `docker` and `docker-compose` installed
1. Create a `config.json` file by duplicating `config.example.json` and modifying the values. For this example, the defaults should work fine with `docker-compose`

## Starting

1. Run `start-docker.sh` to start the containers.

## Stopping

1. Run `stop-docker.sh` to stop the containers.

## Other `docker-compose` commands (such as logs)

Because the `docker-compose` deployment is done with 2 files, you must reference both with the `-f` flag **before** the command option:

```bash
docker-compose -f docker-compose.deps.yaml -f docker-compose.app.yaml logs -f
```

# Viewing the API documentation

Access [http://localhost:8080/api/v1/ui/](http://localhost:8080/api/v1/ui/) on a browser to view the Swagger UI. You can use it to look at the documentation and to test API calls yourself.

# Uploading a data breach

The best way to do it is through the API container after setting up the local deployment.

A `data_breaches` directory has been mapped to the container through a volume, so place any files that are to be uploaded,
and from this directory, run:

```bash
./upload-breach-docker.sh "<Breach Name>" "<File Name in data_breaches dir>"
```

This script will error out if a breach already exists for the given name.

# Stack

## API

- Flask
- Gunicorn 
- Connexion

## Persistence

- MongoDB
- Minio (S3)

## Distributed Systems

- Celery
- RabbitMQ
- Redis

## Deployment

- Docker
- Docker Compose

# Running locally

You can run this outside Docker, provided you have Python 3.7 and `pipenv` installed.

Run `pipenv install` to set things up. It is recommended you use `pipenv`'s Virtual Environment support.

## Dependencies

- A MongoDB instance
- An Object Storage instance, such as Minio
- An AMQP instance, such as RabbitMQ
- A Redis instance

Configure those in `config.json` (you may use `config.example.json` as a base)

Alternatively, use `docker-compose.deps.yaml`. All services map into their default local ports.

## Setting things up

To set things up on the DB and COS, run the following commands:

```bash
python -m have_i_not_been_owned.scripts.setup_s3
python -m have_i_not_been_owned.scripts.setup_db
```

## Running the API

Run the following command:

```bash
python -m have_i_not_been_owned.api
```

It'll be available on port 5000

## Running the Celery workers

Run the following command:

```bash
celery -A have_i_not_been_owned.celery worker -c 4 -l INFO
```

## Alternative scripts

The `scripts/` directory has shell scripts you can use instead. Do mind that the API one will use `gunicorn` rather than the Flask development server.
I prefer the latter whenever possible for debugging purposes.
