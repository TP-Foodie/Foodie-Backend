# Foodie-Backend  [![Build Status](https://travis-ci.org/TP-Foodie/Foodie-Backend.svg?branch=master)](https://travis-ci.org/TP-Foodie/Foodie-Backend)
Application Server

## Docs
- [Release Plan](https://docs.google.com/spreadsheets/d/1V6PulNcmdxFSB4VBtAvh1eBTG40W4kyfb-GfkZr9fRQ/edit?usp=sharing)
- [Board](https://github.com/orgs/TP-Foodie/projects/1)

### Instalar los requerimientos con pip

```pip install -r requirements.txt```

### Correr pylint

```pylint src/```

### Correr pytest

```pytest --cov=src --cov-fail-under=75 --cov-config=.coveragerc```

### Correr la aplicacion con docker-compose

```docker-compose up```

Para forzar que se regeneren las imágenes se tiene que poner `--build`
