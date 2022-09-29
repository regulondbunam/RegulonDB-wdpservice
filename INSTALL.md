
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
Enter the project directory and src and install venv with the following command
```shell
cd regulonDB-wdpservice/src
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
pip install flask flask-cors sgqlc python-dotenv pdfkit
```
dependency wkhtmltopdf
```shell
sudo apt-get install wkhtmltopdf
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


- ### Expected Directory Structure 

[Directory structure after installation. It should be properly organised in sub-directories (for documentation, headers, source, etc.]



- ### Dependencies

[All required or optional dependencies should be listed, including those by third parties (with references to their websites).]


- ### Errors & Tips
[Describe possible errors that can be occur during the installation software and their solution.]
