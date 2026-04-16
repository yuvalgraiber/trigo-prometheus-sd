FROM python:3.14-slim
WORKDIR /app
RUN pip install requests
COPY discovery_adapter.py .
# Use python -u to see print logs in real-time
CMD ["python", "-u", "discovery_adapter.py"]