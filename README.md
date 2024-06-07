# fields_monitoring

# Execute project
## Download dependencies
You have to have installed Poetry, FastAPI, and Localstack to test the S3 storaging.

Enter the poetry shell executing the following command on the project root directory

    poetry shell

Download the dependencies using the command

    poetry install 

Execute the project with reloading feature with the command

    poetry run uvicorn main:app --reload --port 8000

In another terminal window, run Localstack container using the following command

    localstack start


## Using Docker
In order to execute Dockerfile, firstly build the image.

    docker build -t my_image_name .

You can run the container using the following command. This command maps
the 8000 port into the machine 8000 port.

    docker run -it -p 8000:8000 --rm my_image_name

# Swagger
You can access the Swagger documentation using the /docs endpoint.
So if you are using localhost and port 8000, go to the following link

    http://localhost:8000/docs

# Testing
Run the tests entering the environment

    poetry shell

And then execute the command

    pytest