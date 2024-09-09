FROM python:3.10

# Встановимо змінну середовища
ENV APP_HOME /app

# Встановимо робочу директорію усередині контейнера
WORKDIR $APP_HOME

# Копіюємо файли pyproject.toml і poetry.lock у контейнер
COPY pyproject.toml $APP_HOME/pyproject.toml
COPY poetry.lock $APP_HOME/poetry.lockpyh

# Встановимо залежності усередині контейнера
RUN apt-get -y update              ; \
    apt-get -y install curl        ; \
    apt-get -y install wget        ; \
    apt-get -y install git         ; \
    apt-get -y install vim         ; \
    apt-get -y install hdf5-tools  ; \
    apt-get -y install libhdf5-dev ; \
    apt -y install postgresql
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main


# Копіюємо всі інші файли проекту у контейнер
COPY . .

# Позначимо порт, на якому працює програма всередині контейнера
EXPOSE 8000

# Запускаємо нашу програму всередині контейнера
CMD ["python", "parking/manage.py", "runserver", "0.0.0.0:8000"]