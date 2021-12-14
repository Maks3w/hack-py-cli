FROM --platform=linux/amd64 python:3.10.1-slim@sha256:9f702aa0f2bd7fe7a43bcf46e487040ba3237f2115994ae74ea7b270479ea8f3

RUN pip install --no-cache-dir pipenv==2021.11.23

ENV HOMEDIR=/project/src/ \
  TERM=vt100 \
  C_FORCE_ROOT=1 \
  PYTHONUNBUFFERED=1 \
  PIPENV_VERBOSE=True

WORKDIR $HOMEDIR

# PIPENV_ARGS is used to pass arguments to pipenv.
# Ex: --dev for development dependencies
ARG PIPENV_ARGS

COPY src/Pipfile src/Pipfile.lock $HOMEDIR
# Build time required depèndencies are declared in buildDeps var. They are **uninstalled** after build.
RUN buildDeps="" \
  && apt-get update && apt-get install --assume-yes --no-install-recommends \
    $buildDeps \
    # Runtime required dependencies go here \
    # Ex: gcc \
  && pipenv install --system --deploy $PIPENV_ARGS \
  && rm -rf ~/.cache/ \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false $buildDeps \
  && apt-get clean

# Change user (by default "root") for lower privileges while executing the container
USER www-data
