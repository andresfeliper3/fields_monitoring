# fields_monitoring

# Execute project
You can use the .env.example file as reference. The only variable you
necessarily have to change is NASA_API_KEY.
## Download dependencies
You have to have installed Poetry, FastAPI, and Localstack to test the S3 storaging.

Enter the poetry shell executing the following command on the project root directory

    poetry shell

Download the dependencies using the command

    poetry install 

Execute the project with reloading feature with the command. You must change the 
LOCALSTACK_HOST environment variable to http://localhost in order to use it without Docker.

    poetry run uvicorn main:app --reload --port 8000

In another terminal window, run Localstack container using the following command

    localstack start


## Using Docker
In order to execute Dockerfile, firstly build the image.
Change the environment variable LOCALSTACK_HOST to http://host.docker.internal in order to execute it.

    docker build -t my_image_name .

You can run the container using the following command. This command maps
the 8000 port into the machine 8000 port.

    docker run -it -p 8000:8000 --rm my_image_name


Or you can build using the Docker Compose for creating one container for the project
and another container for Localstack.
Change the environment variable LOCALSTACK_HOST to http://localstack in order to execute it.

    docker-compose up --build


# Swagger
You can access the Swagger documentation using the /docs endpoint.
So if you are using localhost and port 8000, go to the following link

    http://localhost:8000/docs

# Testing
Run the tests entering the environment

    poetry shell

And then execute the command

    pytest