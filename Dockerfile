FROM python:3.9.7-slim-buster

# prevent __pycache__ folder and files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Install build deps
RUN set -ex \
  && apt-get update \
  && apt-get install -qq -y --no-install-recommends \
  sudo \
  acl \
  unzip \
  make \
  curl \
  gcc \
  git \
  jq \
  gettext \
  procps \
  python3-dev \
  # heroku dependency
  && apt-get install -qq -y --no-install-recommends openssh-server \
  && pip install pipenv \
  && rm -rf /var/lib/apt/lists/*


COPY Pipfile Pipfile.lock .pre-commit-config.yaml ./
RUN pipenv install --system --deploy --dev

# TODO: Add the below to pipfile
RUN pip install git+https://github.com/iamumairayub/scrapyd-client.git --upgrade

ADD . ./

RUN adduser --disabled-password --gecos '' admin
RUN adduser admin sudo
RUN mkdir /app/dbs /app/eggs && \
    chown -R admin:admin /app && \
    chown -R admin:admin /etc/environment && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    ls -ltrh /app
USER admin

ENTRYPOINT ["/app/docker-entrypoint.sh"]