FROM arm32v7/python:3.10.6-alpine3.16
CMD ["pipenv", "run", "python", "./main.py"]

RUN pip install pipenv
RUN pipenv run pip install selenium webdriver_manager selenium_driver_updater PyYaml

COPY config.yaml ./
COPY main.py ./