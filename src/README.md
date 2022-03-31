# RegulonDB Web Data Prosses Services

welcome n.n/
version 0.2.0

## Description
This service allows data processing from RegulonDB-HT GraphQL API services. It transforms datamat information into CVS, BED, GFF3 and regulonDB specific formats.

## Hardware requirements

### Server

minimum requirements

-   CPU > 2 GHz, 4 cores
-   RAM > 8Gb
-   Space on disk > 5 Gb
-   A connection to the Internet if RegulonDB-HT GraphQL API is not installed on the server

### Client

This application is rendered on server side. Any device that supports connections to a network is supported

minimum requirements

-   A connection to the Internet

## Software Requirements

### server:

-   RegulonDB-HT GraphQL API
-   Python 3.8

### Client

- Chrome 60+
- Safari 10+ / iOS Safari 10+
- Edge 12+
- Firefox ESR+
- Internet Explorer 11
- Opera

## Installation

**Step 1 download project**
You need to download this repository, in its master branch,

```shell
git clone https://github.com/regulondbunam/RegulonDBHT-Web.git
```

You can also download the zip file from the repository and unzip it to a designated location

**Step 2 install venv**
install venv python library
```shell
sudo apt install python3-venv
```
Enter the project directory and install venv with the following command
```shell
python3 -m venv venv
```
**Step 3 activate venv**
on project directory
```shell
. venv/bin/activate
```
**Step 4 install project dependencies**

dependencies: 
- flask
- sgqlc
- flask-cors
- csv
- python-dotenv
```shell
pip install flask flask-cors sgqlc python-dotenv
```
**Step 5 configuration**

At the root of the project, you will find the .envExample file where you will find the information to declare the environment variables so that the application can connect to the regulonDB web services.

duplicate the .env-sample file and rename it to .env and add the information requested in the .envExample file.

``` 
#rename this file to '.env' when the fields have been filled
# GQL_SERVICE = "url of RegulonDB-HT GraphQL API"

GQL_SERVICE=000.000.000.00
```

**Step 6 start service**

You can find more information on how to implement this application in the following link [Flask Minimal Application](https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application)

```shell
export FLASK_APP=app.py
flask run --host=0.0.0.0
```
