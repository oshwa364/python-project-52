build:
    ./build.sh
render-start:
    gunicorn task_manager.wsgi
start:
	uv run manage.py runserver 0.0.0.0:8000