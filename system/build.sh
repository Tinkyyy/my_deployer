sudo docker build -t system:latest .
sudo docker run -d --name system -p 8000:8000 system:latest