# Loyalty service



## Run in Docker
Firstly create `admin.env` and `api.env` files in the root folder of project

`.env` parameters can be found in 
[admin_panel/README.md](./admin_panel/README.md) and 
[loyalty_api/README.md](./loyalty_api/README.md) respectively.

To run api in `Docker` execute following command:
```shell
docker compose up --build
```

OpenApi documentation url: http://localhost/api/openapi/

Admin panel url: http://localhost/admin