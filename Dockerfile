FROM python:3.9-slim
WORKDIR /app

# Install libraries one by one to save progress
# If one fails due to internet, run the build command again to resume!
RUN pip install --default-timeout=1000 --no-cache-dir Flask==3.0.3
RUN pip install --default-timeout=1000 --no-cache-dir numpy==1.26.4
RUN pip install --default-timeout=1000 --no-cache-dir scikit-learn==1.5.0
RUN pip install --default-timeout=1000 --no-cache-dir pandas==2.2.2
RUN pip install --default-timeout=1000 --no-cache-dir matplotlib==3.9.0 seaborn==0.13.2

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
