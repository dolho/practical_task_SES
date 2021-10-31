web: gunicorn server:app --preload
microservice_auth: python3 ./microservices/user_auth/user_auth_service.py:app
microservice_converter: python3 ./microservices/currency_converter/currency_converter_service.py:app
celery: celery --app app.blueprints.user.email_worker  worker --loglevel=INFO
