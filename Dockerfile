FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN DJANGO_SECRET_KEY=build-only-key-not-used-at-runtime python manage.py collectstatic --noinput
RUN useradd --create-home portal && mkdir -p /var/data/media && chown -R portal:portal /app /var/data
USER portal
EXPOSE 8000
CMD ["bash", "start.sh"]
