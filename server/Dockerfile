FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    git  # Example tool (replace with your specific needs)
EXPOSE 8080
CMD ["python", "main.py"]
