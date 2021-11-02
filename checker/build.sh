sudo docker build -t checker:latest .
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -d --name checker -p 8080:8080 checker:latest