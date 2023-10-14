# SchoolAi ReadMe

## Table Of Contents
- [Set up for Local Machine](#set-up-the-server)
- [Base Uri/Live Deployment](#base-uri)
- [Error Handling](#error-handling)
- [EndPoints](#endpoints)
  - [Authentication Routes](#authentication)
      - `/register`
      - `/login`
      - `/@me`
  - [Explanation routes](#explanation-or-chat-completion)
      - `/explain`
      - `/history`
- [Authors](#authors)


## **SchoolAi API-ENDPOINT DOCUMENTATION**
---
<br>
<br>

### **Set up the server**
#### Install Dependencies
```bash
$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r requirements.txt
```
#### if you use pipenv

```bash
$ pip install pipenv

# create virtuel environment
$ pipenv --python 3.10

# Activate virtual env
$ pipenv shell

# install dependencies in requirements.txt or pipfile
$ pipenv install
```

#### Set up the Database

With Postgres running, create a `dbname` database:
or no db setup needed if dburl is not set in .env file as filedb will be created

```bash
$ createdb dbname
```
#### Add env Variables
create .env file and add variables as in [sample.env](sample.env)
do not forget to get your openai api key from platform.openai.com/account/api-keys

#### Run the Server
```bash
$ python3 run.py 
```

### **Base Uri**
----
----
temporarily hosted for live testing on **https://baseuri**
....


<br>

### **Error Handling**
---
---
>Errors are returned as JSON objects in the following format with their error code

```json
{
  "error": "error name",
  "message": "error description",
  "status":false
}
```
The API will return 5 error types, with diffreent descriptions when requests fail;
- 400: Request unprocessable
- 403: Forbidden
- 404: resource not found
- 422: Bad Request
- 429: Too Many Requests(rate limiting)
- 500: Internal server error

<br>



### **EndPoints**
---
---
<br>

#### **AUTHENTICATION**
  > JWT Authorization tokens is used, ensure to add Bearer {jwt token here} in authorization headers gotten after register and login

  `POST '/auth/register'`

- Register new user,
- Request Arguements: JSON object containing
```json
{
  "email":"user email",
  "password":"password at least 8 characters",
  "confirm_password":"confirm password",
}
```
- Returns `message` ,`user name` and `email`
```json
{
    "message": "success",
    "status": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.",
    "user": {
      "date_created": "Sat, 14 Oct 2023 13:42:27 GMT",
      "email": "test3@email.com",
      "id": "0adb2e97fa964d9ead21d210170975e5"
      }
}
```
---
<br>

  `POST '/auth/login/'`
- login user account
- Request Arguements: JSON object containing
```json
{
  "email":"user email",
  "password":"password at least 5 characters",
}
```
- Returns: JSON object containing
```json
{
    "message": "success",
    "status": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.",
    "user": {
      "date_created": "Sat, 14 Oct 2023 13:42:27 GMT",
      "email": "test3@email.com",
      "id": "0adb2e97fa964d9ead21d210170975e5"
      }
}
```

---
<br>

  `GET '/auth/@me/'`
- get account detailes of currenly logged in user
- REQUIRES AUTHORIZATION BEARER TOKEN
- Returns: JSON object containing
```json
{
  "message": "success",
  "status": true,
  "user": {
    "date_created": "Sat, 14 Oct 2023 12:25:13 GMT",
    "email": "test2@email.com",
    "id": "380f18f9739b43c8b2cab1a56c5dab38"
  }
}
```
---
<br>

#### **Explanation or chat completion**

---
<br>

  `POST '/explain'`
- explain each topics in a detailed easy to understand way and save to user history
- REQUIRES AUTHORIZATION BEARER TOKEN
- Request Arguements: JSON object containing array of topics
```json
{
  "topics":["induction motors","the georaphy of asia"]
}
```
- Returns: JSON object containing
```json
{
  "explained_topics": {
    "the georaphy of asia": "Sure! The geography of Asia is incredibly diverse and fascinating. It is the largest continent in the world, covering about 30% of the Earth's land area. Asia is bordered by the Arctic Ocean to the north, the Pacific Ocean to the east, the Indian Ocean to the south, and Europe and Africa to the west.\n\nOne of the most prominent features of Asia is its vast and varied landscape..."
  },
  "message": "sucessfully explianed",
  "status": true
}
```

---
<br>

  `GET '/history'`
- get explanation history or past explanations requested by a user
- REQUIRES AUTHORIZATION BEARER TOKEN
- Returns: JSON object containing
```json
{
  "history": [
    {
      "date_created": "Sat, 14 Oct 2023 12:47:41 GMT",
      "explanation": "Induction motors are a type of electric motor that are commonly used in various applications, such as industrial machinery, household appliances, and even electric vehicles. They work based on the principle of electromagnetic induction.\n\nTo understand how an induction motor ...",
      "topic": "induction motors",
      "id": 5,
      "user": "test2@email.com"
    },
    {
      "date_created": "Sat, 14 Oct 2023 12:48:05 GMT",
      "explanation": "Software development is the process of creating computer programs or applications that perform specific tasks or functions...",
      "topic": "software development",
      "id": 6,
      "user": "test2@email.com"
    },
    {
      "date_created": "Sat, 14 Oct 2023 13:57:02 GMT",
      "explanation": "Sure! The geography of Asia is incredibly diverse and fascinating. It is the largest continent in the world, covering about 30% of the Earth's land area. Asia is bordered by the Arctic Ocean to the north,...",
      "topic": "the georaphy of asia",
      "id": 7,
      "user": "test2@email.com"
    }
  ],
  "message": "success",
  "status": true
}
```


## Authors
- [@Godhanded](https://github.com/Godhanded)

