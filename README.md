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
