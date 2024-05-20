FROM python:3.12.2

WORKDIR /usr/src/app

ENV TZ=Europe/Istanbul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run unit tests
ENV MODEL_FILES_PATH=/usr/src/app/test/test-model-files
RUN python -m unittest discover

ENTRYPOINT ["python", "flask_main.py"]

EXPOSE 8080

#CMD ["gunicorn", "flask_main:app", "-b", "0.0.0.0:8080", "--workers=4", "--threads=2"]