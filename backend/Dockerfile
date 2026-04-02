FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir Flask==3.0.0 flask-cors==4.0.0 python-dotenv==1.0.0 google-generativeai>=0.3.0 numpy>=1.24.0 tqdm>=4.65.0 transformers>=4.30.0

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch>=2.0.0

COPY . .

EXPOSE 10000

CMD ["python", "app.py"]