FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY app/requirements.txt .
RUN uv pip install -r requirements.txt
COPY app/ .
EXPOSE 5000
CMD ["python", "app.py"]