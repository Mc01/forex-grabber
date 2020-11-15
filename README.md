# Forex grabber

Apps that grab latest forex prices from OpenExchangeRates API

## Setup

Fill secrets
```
cp .secret.sample .secret && nano .secret
```

Build and run app with command:
```
docker-compose up -d
```

Create database
```
docker-compose exec app flask create-db
```

Apply migrations
```
docker-compose exec app flask db upgrade
```

## Formatters

Black
```
docker-compose exec app black .
```

iSort
```
docker-compose exec app isort --atomic .
```

## Run tests

Start tests with command:
```
docker-compose run app pytest
```

## Endpoints

Following endpoints are available:

```
- url: /grab_and_save
- method: POST
- required argument: currency
- required argument: amount
```

```
- url: /last
- method: GET
- optional argument: currency
- optional argument: number
- request examples:
> curl -X GET "http://localhost:5000/last"
> curl -X GET "http://localhost:5000/last?currency=AED"
> curl -X GET "http://localhost:5000/last?number=3"
> curl -X GET "http://localhost:5000/last?currency=AED&number=3"
```

## Note

Please check `final_amount` calculation notes in `GrabAndSave` resources in `resources.py`
