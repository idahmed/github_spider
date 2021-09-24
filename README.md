## Overview



## Developer Guide

### Generate Google Service Token

1. Place `credentials.json` in root directory
2. Run `script google_generate_token.py`

Follow the steps, the script will generate the `token.json` file in the root directory.

**Note: the above steps should be done in console and cannot be ran from docker-compose due to the authentication with google and CLI**

### `docker-compose`

```bash
# bring up services
# This is required to add support for some ARGs defined in Dockerfile
export DOCKER_BUILDKIT=1
docker-compose build
docker-compose up -d
```

- Scrapyd: http://127.0.0.1:6800
