FROM python:3.11

# Set the working directory to the root directory where Dockerfile is located
WORKDIR /

# Copy the pyproject.toml and poetry.lock files into the working directory
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add Poetry executable paths to the system PATH
ENV PATH="/root/.poetry/bin:/root/.local/bin:${PATH}"

# Install project dependencies with Poetry
RUN poetry install

# Copy the rest of the project files into the working directory
COPY . .

# Command to run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
