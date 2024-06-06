FROM python:3.11

# Set the working directory to the root directory where Dockerfile is located
WORKDIR /

# Copy the pyproject.toml and poetry.lock files into the working directory
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add Poetry executable path to the system PATH
ENV PATH="/root/.poetry/bin:${PATH}"

# Install project dependencies with Poetry


# Copy the rest of the project files into the working directory
COPY . .

# Command to run the application
CMD ["python", "app.py"]
