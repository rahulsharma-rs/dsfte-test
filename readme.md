# This file lets you kno about the project

## how to run the project
### to run the project you need to install the following packages
```pip install -r requirements.txt```
### to run the project use the following command
```python app.py```

### to run with flask use the following command
```cd dsfet-flask```
```export FLASK_APP=app/app.py```
```flask run```

## Docker related commands
### to create the container use the following command 
```docker build -t flaskapp:latest .```

### using the following commands you can run the project
```docker run -d -p 5001:5000 --runtime=runc -d flaskapp:latest```