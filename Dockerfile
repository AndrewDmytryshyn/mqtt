# set base image (host OS)
FROM python:latest
# copy the content of the local src directory to the working directory
COPY . .
# install dependencies
RUN pip install -r labb1/requirements.txt
# command to run on container start
CMD ["python", "labb1/main.py"]
