# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

# Set the home directory to root
ENV HOME /root

# cd into home directory
WORKDIR /root

# Copy all app files into the image
COPY . .

# Download dependencies
RUN pip3 install -r requirements.txt

# Allow port 8000 to be accessed from outside the container
EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# Run the app
# During debugging, this entry point will be overriden
CMD /wait && python3 server.py