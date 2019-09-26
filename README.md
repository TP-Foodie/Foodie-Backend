# Foodie-Backend  [![Build Status](https://travis-ci.org/TP-Foodie/Foodie-Backend.svg?branch=master)](https://travis-ci.org/TP-Foodie/Foodie-Backend) [![Coverage Status](https://coveralls.io/repos/github/TP-Foodie/Foodie-Backend/badge.svg?branch=master)](https://coveralls.io/github/TP-Foodie/Foodie-Backend?branch=master)
Application Server

## Docs
- [Release Plan](https://docs.google.com/spreadsheets/d/1V6PulNcmdxFSB4VBtAvh1eBTG40W4kyfb-GfkZr9fRQ/edit?usp=sharing)
- [Board](https://github.com/orgs/TP-Foodie/projects/1)

### Swagger

- [Documentacion de la API](https://t2-foodie-server.herokuapp.com/swagger)

### Instalar los requerimientos con pip

```pip install -r requirements.txt```

### Correr pylint

```pylint src/```

### Arreglar automaticamente los errores de estilos

```
find src/ -name "*.py" | xargs -n 1 -P 8 -t -I{} autopep8 -v --in-place --aggressive --aggressive --max-line-length 100 {}
find test/ -name "*.py" | xargs -n 1 -P 8 -t -I{} autopep8 -v --in-place --aggressive --aggressive --max-line-length 100 {}
```

### Correr pytest

```pytest --cov=src --cov-fail-under=75 --cov-config=.coveragerc```

### Correr la aplicacion con docker-compose

```docker-compose up```

Para forzar que se regeneren las imágenes se tiene que poner `--build`
