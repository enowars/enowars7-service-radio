# Use a suitable base-image.
FROM python:3-alpine

# Create a seperate user and chown new directories if necessary
RUN addgroup --system service
RUN adduser --system --ingroup service --uid 1000 service

# Create our mapped data volume endpoint
RUN mkdir /data/
# Copy our service
COPY src/ /service/
# Change the working directory.
WORKDIR /service/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
# Expose the service's port
EXPOSE 8000
# Make flask external visible
CMD ["flask", "--app" , "server", "run", "--host=0.0.0.0"]