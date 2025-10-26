FROM python:3.13.8-slim
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . .
EXPOSE 8001
CMD ["fastapi", "run", "local/task1.py", "--port", "8001"]
