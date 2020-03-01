FROM python:3.7-buster AS build

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy --system

FROM python:3.7-slim-buster

# Add user, create directory for our app code, and install gosu to step down from root
RUN useradd -ms /bin/bash hinbo \
    && mkdir /app \
    && chown hinbo:hinbo /app \
    && apt-get update \
    && apt-get install gosu \
    && gosu nobody true

# Copy previously installed packages on the build stage
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages

WORKDIR /app

COPY --chown=hinbo:hinbo .docker/docker-entrypoint.sh /usr/local/bin

COPY --chown=hinbo:hinbo have_i_not_been_owned .

CMD ["gosu", "hinbo:hinbo", "docker-entrypoint.sh"]

