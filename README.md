## Script for get average salary from "HeadHunter and Superjob" search and recruitment services

Project for to receive an average salary in programming languages,
 from the services of [HeadHunter](https://hh.ru/) and [Superjob](https://www.superjob.ru/).

## Getting Started

For the project to work, install all necessary packages from `requirements.txt`.

```python
pip install -r requirements.txt
```

For work with API register and get the SECRET_KEY from the site https://api.superjob.ru/
don`t need key for work with another service.

```python
SJ_SECRET_KEY='your key'
```
you extract it in the code with package `import os`.

```python
import os
from dotenv import load_dotenv


main()
load_dotenv(verbose=True)
secret_key = os.getenv('SJ_SECRET_KEY')
headers_sj = {'X-Api-App-Id': secret_key}
```
The [terminaltables](https://pypi.org/project/terminaltables/) library was used to output data in a table.

## Motivation

The project is an assignment in online courses [Devman](https://dvmn.org/modules/).

## Running

The script is run from the command line.

```python
python work_parser.py
```

## License

You may copy, distribute and modify the software.
