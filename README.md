# ot_coap
1. Install required packages:
```
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv
```
2. Create virtual environment.
```
python3 -m venv ot_coap_env
source ot_coap_env/bin/activate
```
3. Install packages:
```
pip3 install wheel
pip3 install -r requirements.txt
```
4. Check Flask application:
```
gunicorn --bind 0.0.0.0:5000 ot_coap_wsgi:app
```
5. Create Gunicorn service:
```
sudo cp ./ot_coap.service /etc/systemd/system/ot_coap.service
``` 
6. Create COAP server service:
```
sudo cp ./ot_coap_server.service /etc/systemd/system/ot_coap_server.service
```
7. Start services:
```
sudo systemctl start ot_coap.service
sudo systemctl start ot_coap_server.service

```
8. Configure NGINX
```
sudo vim /etc/nginx/sites-available/ot_coap 
```
  
```
server {
    listen 8080;
    server_name 192.168.2.5;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/debian/workspace/ot_coap/ot_coap.sock;
    }
}

```

Start:
```
sudo ln -s /etc/nginx/sites-available/ot_coap /etc/nginx/sites-enabled/
```
Check for errors:

```
sudo nginx -t
```

 


