Run backend:
Open anaconda prompt and navigate to mushroom-mate folder
Run the virtual environment with the command: 
```bash
.\venv\Scripts\activate
```

If you don't have it create it and install the requirements.txt:

```bash
python -m venv venv
pip install -r requirements.txt
```

Then run the comand
```bash
python app.py
```

Run frontend:

Open CMD and run 
```bash
npm install
npm install react react-dom
npm install -D vite-plugin-react @vitejs/plugin-react-refresh tailwindcss@latest postcss@latest autoprefixer@latest

npm start

npm run dev
```

**Create an EC2 Instance:**

Launch an EC2 instance using the AWS Management Console.
Choose an AMI (Amazon Machine Image), like Ubuntu Server.
Configure instance details, add storage, and configure security groups to allow HTTP (port 80), HTTPS (port 443), and SSH (port 22).

Comands for AWS EC2 Instance
IMPORTANT! Add all permissions to the files and folders needed to be used by the webserver (NGINX) en nuestro caso:

Connect to Your Instance:
Use SSH to connect to your instance. Run this in CDM:
```bash
ssh -i "C:/Users/mario/Downloads/mushroom-mate-passwords.pem" ec2-user@ec2-16-171-253-88.eu-north-1.compute.amazonaws.com
```

Clone the git repo:
```bash
git clone -b master https://github.com/mariolallana/mushroom-mate
```

NGINX configuration file:
```bash
server {
    listen 80;
    server_name 16.171.253.88;

    root /home/ec2-user/mushroom-mate/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://unix:/home/ec2-user/mushroom-mate/backend/mushroom-mate.sock;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

}
```

BACKEND WEB SEVER:
```bash
gunicorn --workers 3 --bind unix:/home/ec2-user/mushroom-mate/backend/mushroom-mate.sock -m 007 app:app
gunicorn --workers 3 --bind unix:mushroom-mate.sock -m 007 app:app
```

1. Verify Gunicorn is Running and Listening
First, ensure that Gunicorn is running and listening on the correct socket file:
```bash
ps aux | grep gunicorn
```

2. Check Socket File Permissions
Ensure that the socket file created by Gunicorn has the correct permissions that allow NGINX to read and write to it. Typically, the NGINX and Gunicorn should run under the same group or NGINX should have the necessary permissions to access the socket file.

To check the socket file permissions, use:
```bash
ls -l /path/to/your/mushroom-mate.sock
If needed, adjust the permissions. For example, you can change the group to nginx and set the appropriate permissions:
```

```bash
sudo chgrp nginx /path/to/your/mushroom-mate.sock
sudo chmod 770 /path/to/your/mushroom-mate.sock
```

4. Check for SELinux Issues
If you're on a system with SELinux enabled, it could be preventing NGINX from accessing the Gunicorn socket file.

To see if SELinux is the cause, check its mode:
```bash
getenforce
```

If it returns Enforcing, you can temporarily set it to Permissive to see if it resolves your issue (note: this is for debugging purposes; you should configure proper SELinux policies instead of leaving it permissive):
```bash
sudo setenforce 0
```

Every time you configure or change something in the server:
```bash
sudo systemctl reload nginx
```

Run Gunicorn 

API Tests:
```bash
curl http://16.171.253.88/api/weather-data
```


