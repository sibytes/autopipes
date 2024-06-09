<img src="https://img.shields.io/badge/Python-v3.8-blue">

# Documentation

https://autopipes.readthedocs.io/en/latest/

# Development Setup

Create virual environment and install dependencies for local development:

```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# Configuration & Authentication


Exporting variables doesn't make for a great development experience so the project uses pytest.ini for
mock environment variables. For example:

```
[pytest]
env =
    DATABRICKS_API_HOST=https://<my_databricks_host>.azuredatabricks.net
    DBUTILSTOKEN=<my_token>
    ...
```

**REMINDER: do NOT commit pytest.ini that contains real security tokens**

For convenience here is a yaml template for docker and build pipelines:

# Build

Build python wheel:
```
python setup.py sdist bdist_wheel
```

There is a CI build configured for this repo that builds on main origin and publishes to PyPi.

# Test

Dependencies for testing:
```
pip install --editable .
```

Run tests:
```
pytest
```

Test Coverage:
```
pytest --cov=autopipes --cov-report=html
```

View the report in a browser:
```
./htmlcov/index.html
```


