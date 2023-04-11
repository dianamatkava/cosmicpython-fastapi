# trafficArbitrationForm
Form of traffic arbitration

11.04.2023

## Create and activate virtual environment:
```bash
python3 -m venv venv
venv\Scripts\activate (Windows in CMD)
source venv/bin/activate (Linux)
```


## Install dependensies for backend:
```bash
pip install -r requirements.txt
```

## Run server:
```bash
flask --app app --debug run
```

## Init DB:
```bash
flask db init
flask db migrate
flask db upgrade
```

# Examples
[Figma Design](AbritrageTraffic.pdf)