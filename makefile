frontend:
	CONFIG_FILE_PATH=../config.py flask --app frontend run -p 5001 --debug	

backend:
	CONFIG_FILE_PATH=../config.py flask --app backend run -p 5000 --debug	