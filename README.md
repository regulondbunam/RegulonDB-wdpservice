# RegulonDB Web Data Prosses Services

welcome n.n/
version 0.4.1

## Description
This service allows data processing from RegulonDB-WebService GraphQL API services. It transforms datamat information into CVS, BED, GFF3 and regulonDB specific formats.

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
-   RegulonDB-Browser
-   Python 3.8
-   wkhtmltopdf
-   google-chrome

#### Install Dependencies server

```shell
apt-get install wkhtmltopdf

apt-get install xvfb

apt-get install fonts-liberation libasound2 libnspr4 libnss3 wget xdg-utils

```

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
on Windows
```sell
pip install virtualenv
```
Enter the project directory and creates the virtual runtime environment
```shell
python3 -m venv venv
```
on Windows
```shell
virtualenv venv

```

**Step 3 activate venv**
on project directory
```shell
. venv/bin/activate
```
On windows you need to modify about_Execution_Policies to allow the execution of the venv script, visit https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2.
for more information
```shell
./venv/Scripts/activate
```
**Step 4 install project dependencies**

```shell
pip install -r requirements.txt
```
**Step 5 configuration**

At the root of the project, you will find the .envExample file where you will find the information to declare the environment variables so that the application can connect to the regulonDB web services.

duplicate the .env-sample file and rename it to .env and add the information requested in the .envExample file.

``` 
#rename this file to '.env' when the fields have been filled
# GQL_SERVICE = "url of RegulonDB GraphQL API"
# REGULONDB_BROWSER = "url of RegulonDB Browser, use this element to create image web"

GQL_SERVICE=http://000.000.000.00
REGULONDB_BROWSER=http://127.0.0.1/
```

**Step 6 start service**

You can find more information on how to implement this application in the following link [Flask Minimal Application](https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application)

```shell
export FLASK_APP=app.py
flask run --host=0.0.0.0
```
Development note, if you are using visual code you have to execute the following command "pip install Flask-Session" before entering venv, and to debug mode "export FLASK_DEBUG=1"
debug on linux
```shell
export FLASK_DEBUG=1
```
debug on windows
```shell
 $env:FLASK_DEBUG = "1"
 set FLASK_DEBUG=1
 flask run --host=0.0.0.0
```
