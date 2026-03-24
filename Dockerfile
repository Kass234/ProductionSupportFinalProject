# min image Python
FROM python:3.11-slim

# working dir in container
WORKDIR /app

# copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy whole project
COPY . .

# port export
EXPOSE 5000

# start command
CMD ["python", "app.py"]
