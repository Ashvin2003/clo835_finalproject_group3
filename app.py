from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3
import requests
import logging
from botocore.exceptions import ClientError
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Environment variables from ConfigMap and Secrets
DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT", "3306"))
BACKGROUND_IMAGE_URL = os.environ.get("BACKGROUND_IMAGE_URL") or ""
USER_NAME = os.environ.get("USER_NAME") or "Senindu Mendis"
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD, 
    db=DATABASE
)

output = {}
table = 'employee'

# Function to download background image from S3
def download_background_image():
    """Download background image from S3 and save it locally"""
    if not BACKGROUND_IMAGE_URL:
        logger.warning("No background image URL provided")
        return None
    
    try:
        # Parse S3 URL
        parsed_url = urllib.parse.urlparse(BACKGROUND_IMAGE_URL)
        bucket_name = parsed_url.netloc
        object_key = parsed_url.path.lstrip('/')
        
        logger.info(f"Downloading background image from S3: {BACKGROUND_IMAGE_URL}")
        
        # Create S3 client
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        
        # Download the image
        local_path = "/app/static/images/background.jpg"
        s3_client.download_file(bucket_name, object_key, local_path)
        
        logger.info(f"Successfully downloaded background image to {local_path}")
        return "/static/images/background.jpg"
        
    except ClientError as e:
        logger.error(f"Error downloading image from S3: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error downloading image: {e}")
        return None

# Download background image on startup
background_image_path = download_background_image()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', 
                         background_image=background_image_path,
                         user_name=USER_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', 
                         background_image=background_image_path,
                         user_name=USER_NAME)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        logger.info(f"Added employee: {emp_name}")

    except Exception as e:
        logger.error(f"Error adding employee: {e}")
        return render_template('addempoutput.html', 
                             name="Error adding employee", 
                             background_image=background_image_path,
                             user_name=USER_NAME)
    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', 
                         name=emp_name, 
                         background_image=background_image_path,
                         user_name=USER_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", 
                         background_image=background_image_path,
                         user_name=USER_NAME)

@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
            logger.info(f"Retrieved employee: {output['first_name']} {output['last_name']}")
        else:
            logger.warning(f"No employee found with ID: {emp_id}")
            return render_template("getempoutput.html", 
                                 id="Not Found",
                                 fname="Not Found", 
                                 lname="Not Found", 
                                 interest="Not Found", 
                                 location="Not Found",
                                 background_image=background_image_path,
                                 user_name=USER_NAME)
        
    except Exception as e:
        logger.error(f"Error fetching employee data: {e}")
        return render_template("getempoutput.html", 
                             id="Error",
                             fname="Error", 
                             lname="Error", 
                             interest="Error", 
                             location="Error",
                             background_image=background_image_path,
                             user_name=USER_NAME)

    finally:
        cursor.close()

    return render_template("getempoutput.html", 
                         id=output["emp_id"], 
                         fname=output["first_name"],
                         lname=output["last_name"], 
                         interest=output["primary_skills"], 
                         location=output["location"],
                         background_image=background_image_path,
                         user_name=USER_NAME)

if __name__ == '__main__':
    # Log background image URL
    logger.info(f"Background image URL: {BACKGROUND_IMAGE_URL}")
    logger.info(f"User name: {USER_NAME}")
    logger.info(f"Database host: {DBHOST}")
    logger.info(f"Database port: {DBPORT}")
    
    app.run(host='0.0.0.0', port=81, debug=True)
