# Fast api uses persitences with Keycloak

# Run
uses poetry
`poetry shell`
`fastapi dev fastapi-ex-user/main.py`


# Run Keycloak
docker compose up -d

or

docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev

import the realm manually.

## get token
`./token.sh`

# REST calls

```
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "service-account-fastapi-client",
  "email": "service-account-fastapi-client@example.com",
  "password": "test"
}'
```