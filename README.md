# Backend for Storing Images in Flaks

This is the backend microservice of my project, responsible for hanlding API request, uploading images to an S3 bucket, and using Flask as the web framework
Docker for containing the website and connecting to SQLite for data storage.

## Features

- Exposes API endpoints for operations
- Integrates with AWS S3 to store images.
- Utilizes SQLite to keep track of all images uploaded.
- All containirez with Docker

## Prerequisistes

Before running the app, ensure that you have the following set up:

- Python 3.10: Install Python using the official website.
- Docker (Latest Version)
- AWS cli: Install from AWS website, and get your own credentials like Access_key and Secret_access_key(set up permissions as needed)

## Installation

1. Clone Repo

```
git clone git@github.com:TeoOrt/backend_aqo.git
```

2. Navigate inside repo

```
cd backend_aqo
```

3. Set up virtual enviroment (MacOS / Linux)

```
python -m -venv venv
source venv/bin/activate
```

4. Install dependencies

```
pip install -r requirements.txt
```

5. Set up enviroment variables in an .env file
   AWS_ACCESS_KEY_ID = CREDENTIALS
   AWS_SECRET_ACCESS_KEY= CREDENTIALS

6. Run the app

```
python app.py
```

## API Endpoints

- /upload (POST Request) you will upload an image along with some metadata to an aws s3 bucket
- /image-gallery (GET) you will get all of the images that are not in the category of <b> Test<b> since that is for debugging only.

## Docker

1. Build image

```
docker build -t name_of_app .
```

2. Run the container

```
docker run -p 5000:5000 --env-file .env name_of_app
```
