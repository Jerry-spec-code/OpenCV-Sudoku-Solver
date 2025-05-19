ifeq ($(OS),Windows_NT)
	PYTHON3_EXE := python
	ACTIVATE_VENV := . venv/Scripts/activate
else
	PYTHON3_EXE := python3
	ACTIVATE_VENV := . venv/bin/activate
endif

install_frontend::
	(cd ./client && npm install)

start_frontend::
	(cd ./client && npm start)

frontend::
	make install_frontend && make start_frontend

clean_backend::
	(cd ./server && rm -rf venv)

install_backend::
	(cd ./server \
	&& $(PYTHON3_EXE) -m venv venv \
	&& $(ACTIVATE_VENV) \
	&& $(PYTHON3_EXE) -m pip install --no-deps --no-cache-dir -r requirements.txt)

start_backend::
	(cd ./server && $(ACTIVATE_VENV) && $(PYTHON3_EXE) app.py)

backend::
	make install_backend && make start_backend