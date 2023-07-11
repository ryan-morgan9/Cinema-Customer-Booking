# Create the base Python image.
# Here we use the latest version of Python with the slim version.
FROM python:3.10-slim
# Set the environment variable
ENV PYTHONUNBUFFERED 1
# Update the packages
RUN apt-get update
# Install other packages needed for Django
RUN apt-get install python3-dev default-libmysqlclient-dev gcc -y
# As root, create 'desdcustomer' directory
RUN mkdir /desdcustomer
# Set the working directory to '/desdcustomer'
WORKDIR /desdcustomer
# Copy the requirements .txt file to the '/desdcustomer' directory .
COPY requirements.txt ./
# Install the requirements
RUN pip install -r requirements.txt
# Copy the other files in the project to the '/desdcustomer' directory .
COPY . .
# Tell the container to listen on port 8000
EXPOSE 8000
# Command to be executed when starting acontainer
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
