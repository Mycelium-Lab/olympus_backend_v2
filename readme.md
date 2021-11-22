<!-- markdownlint-disable no-inline-html first-line-h1 -->

<div align="center">
  <a href="https://app.olympusdao.finance/#/dashboard" target="_blank">
    <img width="150" src="./img/android-chrome-192x192.png">
  </a>
  <h1>Olympus Monitoring Back End</h1>
</div>


## Running the server

Run

```
docker-compose up -d --build
```

## Installing the utils and libraries

```bash
sudo apt install screen
python3 -m pip install web3, asyncio
screen -S notifications
```
then Ctrl+A+D

## Running the notifications 

```bash
screen -x notifications
cd notifications/loops
python3 event_transfers.py
```
then Ctrl+A+D

## API documentation

http://127.0.0.1:8000/docs


## Testing the code

```
docker-compose exec app python -m pytest app/tests
```

## How to reg/auth

### Registration

Request:
```bash
curl -X POST "https://127.0.0.1:8080/sign-up" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"email\":\"user@example.com\",\"name\":\"string\",\"password\":\"string\"}"
```

Response example:

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "string",
  "token": {
    "access_token": "7537db84a0544080b465f04677817aaf",
    "expires": "2021-11-12T14:02:35.335633",
    "token_type": "bearer"
  }
}
```


### Authentication

Request:
```bash
curl -X POST "https://127.0.0.1:8080/auth" -H  "accept: application/json" -H  "Content-Type: application/x-www-form-urlencoded" -d "grant_type=&username=user%40example.com&password=string&scope=&client_id=&client_secret="
```

Response example:
```json
{
  "access_token": "5a476cab07d04b8e97277f5f379bf299",
  "expires": "2021-11-12T14:20:43.702821",
  "token_type": "bearer"
}
```

### Check if authorized

Request:
```bash
curl -X GET "http://127.0.0.1:8000/users/me" -H  "accept: application/json" -H "Authorization: Bearer {token}"
```

Response (authorized):
```json
{
  "id": 0,
  "email": "user@example.com",
  "name": "string"
}
```

Response (unathorized)
```json
{
  "detail": "Not authenticated"
}
```

Authentication is currently disabled for all routes because not all subgraph parsers have been migrated to pyhton from javascript. If you would like to enable authentication, please check out the example in /app/routers/api.py

Response (unathorized)
```json
{
  "detail": "Not authenticated"
}
```
