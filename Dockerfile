FROM python:3.11-slim
RUN pip install uv
WORKDIR /app
COPY app/requirements.txt .
RUN uv pip install --system -r requirements.txt
COPY app/ .
ENV PORT=5050
EXPOSE 5050
CMD ["python", "app.py"]