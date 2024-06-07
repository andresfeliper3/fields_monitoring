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



# Testing
Run the tests entering the environment

    poetry shell

And then execute the command

    pytest