# testing-server-flask
> Client requested to create a single page with contact form and description section for product
> [11.04.2023] "Get loan in Georgia" deployed [>>>](https://credit-georgia.info/ge) 

# Backend Set Up
##### Create and activate virtual environment:
```bash
python3 -m venv venv
venv\Scripts\activate (Windows in cmd)
source venv/bin/activate (Linux)
```

##### Install dependensies:
```bash
pip install -r requirements.txt
```

##### Envs:
> find .env.sample file in root folder and rename to .env

##### Init DB:
```bash
flask db init
flask db migrate
flask db upgrade
```

##### Run server in development mode:
```bash
flask --app app --debug run
```

# Frontend Set Up 
##### Install dependencies:
``` bash
sudo apt-get install npm (Linux)
```
(For Windows) Download and install Node.js from the official [website](https://nodejs.org/en/download/)
``` bash
npm i tailwindcss
```
##### Build tailwind css:
``` bash
npx tailwindcss -i ./static/css/index.css -o ./static/css/output.css
```
##### Watch for tailwind css updates:
``` bash
npx tailwindcss -i ./static/css/index.css -o ./static/css/output.css --watch
```