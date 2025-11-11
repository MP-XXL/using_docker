FROM python:3.13.8-slim
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . .
EXPOSE 8000
CMD ["fastapi", "run", "main_app/main.py", "--host", "0.0.0.0", "--port", "8000"]
