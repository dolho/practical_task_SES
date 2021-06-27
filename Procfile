web: gunicorn server:app
celery: celery --app app.blueprints.user.email_worker  worker --loglevel=INFO
