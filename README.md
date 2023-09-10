# benford-flask-docker

### Build application
Build the Docker image manually by cloning the Git repo. It is assumed docker is already installed. If not, then please [visit site](https://www.docker.com/products/personal/) to download and install docker. 
```
git clone https://github.com/hth/benford-flask-docker.git
docker build -t benford-flask-docker . && docker compose up
```

Now visit http://localhost:8080
```
 Home screen shows containers hostname and IP address with status of Mongo DB connection 
```
Sample application does following things:
1) Upload files
2) Parses the uploaded file
3) Autocorrects during parsing
4) Generate results
5) Saves result to MongoDB (Skipped on saving file to AWS S3)
6) Shows the result and represent data in graphical form
7) Ajax call to show the history from DB
8) Lists errors found in the file
9) Any other relevant information is displayed
10) Does logging


### Other helpful commands

    docker ps
    docker inspect benford-mongo
    docker restart 932c945e807d 
    docker build -t benford-flask-docker .


### Run the container standalone
Create a container from the image.
```
docker run --name benford-flask-docker-instance  -d -p 8080:8080 benford-flask-docker
```

### Data file
Sample files [census_2009.txt](sample-data%2Fcensus_2009.txt) & [StateTown7_2009.txt](sample-data%2FStateTown7_2009.txt) to test Benford's Law

### Referred during development 
[Init after web application has started](https://stackoverflow.com/questions/27465533/run-code-after-flask-application-has-started) & [Docker Setup](https://dev.to/alissonzampietro/the-amazing-journey-of-docker-compose-17lj)

