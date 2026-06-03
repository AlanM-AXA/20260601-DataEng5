FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app_refactored.py /app/app_refactored.py
COPY run_cleaner.py /app/run_cleaner.py
COPY data /app/data
ENTRYPOINT ["python", "/app/run_cleaner.py"]