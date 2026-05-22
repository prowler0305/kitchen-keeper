FROM python:3.11-slim
LABEL authors="Andrew Spear"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]