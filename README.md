# trafficArbitrationForm
Form of traffic arbitration

11.04.2023

## Create and activate virtual environment:
```bash
python3 -m venv venv
venv\Scripts\activate (Windows in cmd)
source venv/bin/activate (Linux)
```


## Install dependensies for backend:
```bash
pip install -r requirements.txt
```

## Run server in development mod:
```bash
flask --app app --debug run
```

# Front end
## Build tailwind css
``` bash
npx tailwindcss -i ./static/css/index.css -o ./static/css/output.css
```

## Watch tailwind css
``` bash
npx tailwindcss -i ./static/css/index.css -o ./static/css/output.css --watch
```

<!-- ## Init DB:
```bash
flask db init
flask db migrate
flask db upgrade
``` -->

# Examples
[Figma Design](./static/pdf/AbritrageTraffic.pdf)