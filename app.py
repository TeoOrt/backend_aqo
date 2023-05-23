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


# NOTES - Setting up the database and the Flask App


from flask import Flask, request, jsonify
from flask_cors import CORS
from src.aws import AWS_S3
from src.sqlite import Gallery
app = Flask(__name__)
CORS(app)
# Init S3 Client


aws = AWS_S3()

# init SQLite db

gallery = Gallery()
gallery.create_table()


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
    return "LEtttsssss goooo Raytheon"


@app.route('/test', methods=['GET'])
def read_all():
    return jsonify(gallery.show_table())


@app.route('/image-gallery', methods=['GET'])
def retrieve_gallery():
    return gallery.retreive_images()


@app.route("/debug-delete", methods=['GET'])
def delete():
    gallery.delete_section()
    return "Deleted Debugging"


# The main
# Create table is to create the table if the container doesn't have it
if __name__ == '__main__':

    app.run(debug=True)
