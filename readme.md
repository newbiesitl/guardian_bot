# dependency
- `conda install numpy`
- `conda install aiofiles`
- `pip install keyboard`
- `conda install -c conda-forge pyautogui`
- `pip install fastapi`
- `pip install pillow`
- `pip install python-multipart`


# multi boxing tools
## key boardcasting
- Keyclone
https://solidice.com/downloads/windows/keyclone

# run server
`cd app && uvicorn main:app && cd -`

list all ports ps
- `lsof -i:8000`

kill them
- `kill -9 $(lsof -t -i:8000)`

# run client

`python worker_client.py screenshot`

`python worker_client.py keyboard`


# api doc location

`http://127.0.0.1:8000/docs`


# docker
- `docker build -t guardian_bot_server .`
- `docker run -d --name myserver -p 80:80 guardian_bot_server`
- `docker container stop myserver`
- `docker container rm myserver myserver`
