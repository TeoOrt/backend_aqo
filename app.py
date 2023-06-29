"""

Purpose: Backend to server client images and store data
Backend: Create an API for our front end store to load all of the images

Why use backend to load pictures?
Because we want to keep our cost down of our data in our server
Therefore making it better to access our database instead of our 
Server

Will this api be able to fetch userdata?
Yes! That's correct this api will be a quick template to access data
and for our server to render all of the images, and be able to update in realtime

"""


"""
Important Changes 

Storing Images in a S3 bucket in aws

In the database we are going to store the meta data such as price, title, etc.


"""
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from src.aws import AWS_S3
import os
from src.sqlite import Gallery
app = Flask(__name__)
CORS(app)

#  NOTE Init for everything
aws = AWS_S3()
gallery = Gallery()
gallery.create_table()


""" - NOTE  Upload Image
Keyword arguments:
argument -- Front end upload, title, image, cost, and category,
Test will be ignored, but still uploaded
"""


@app.route('/upload', methods=['POST'])
def upload_image():
    img_file = request.files['image']
    # upload to s3
    temp_filename = aws.change_image(img_file)
    # inside this function is has the upload to s3
    # extract meta date from request

    args = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'category': request.form.get('category'),
        'image': temp_filename
    }

    # reason for function to be outside is for better readability
    gallery.upload_to_db(**args)
    return "Completed upload"


@app.route('/image-gallery', methods=['GET'])
def retrieve_gallery():

    return gallery.retreive_images()


@app.route("/get-catalog", methods=['GET'])
def retrieve_cat():
    return gallery.retrieve_catalog()


# The main
# Create table is to create the table if the container doesn't have it
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
