FROM python:3.10-alpine3.17
CMD ["pipenv", "run", "python", "./main.py"]

RUN pip install pipenv
RUN pipenv run pip install selenium webdriver_manager selenium_driver_updater PyYaml

COPY config.yaml ./
COPY EsportsCapsuleFarmer EsportsCapsuleFarmer
COPY main.py ./
