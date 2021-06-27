web: gunicorn server:app --preload
celery: celery --app app.blueprints.user.email_worker  worker --loglevel=INFO
