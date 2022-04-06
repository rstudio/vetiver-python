# #
FROM python:3.8

# #
WORKDIR /code

# #
COPY vetiver_requirements.txt /code/requirements.txt

# #
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# #
COPY . /code/app

# #
CMD ["uvicorn", "app.app:api", "--host", "0.0.0.0", "--port", "80"]
    
