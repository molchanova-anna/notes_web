FROM python:3.8-bookworm

RUN pip install pipenv

WORKDIR /notes_web
ENV PYTHONPATH=./

COPY Pipfile Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install  --system --deploy

COPY . .

EXPOSE 8080:80

CMD ["uvicorn", "main:notes_app", "--host", "0.0.0.0", "--port", "80"]
