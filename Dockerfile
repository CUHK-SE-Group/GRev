FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
#ENV MY_ENV_VAR=my_value
EXPOSE 8080
CMD ["python", "app.py"]
