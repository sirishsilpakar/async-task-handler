# Pull official Python image
FROM python:3.11.2-slim-buster

# Set the work directory
WORKDIR /usr/src/app

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# # Run the application
# CMD ["python", "main.py"]