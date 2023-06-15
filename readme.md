## This file lets you kno about the project

### to create the container use the following comand 
```docker build -t flaskapp:latest .```

### using the following commands you can run the project
```docker run -d -p 5001:5000 --runtime=runc -d flaskapp:latest```