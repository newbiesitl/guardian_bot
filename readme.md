# dependency
- `conda install numpy`
- `conda install aiofiles`
- `pip install keyboard`
- `conda install -c conda-forge pyautogui`
- `pip install fastapi`
- `pip install pillow`
- `python-multipart`

# run server
uvicorn worker_client:app

list all ports ps
`lsof -i:8000`
kill them
`kill -9 $(lsof -t -i:8000)`

# run client

`python worker_client.py screenshot`

`python worker_client.py keyboard`


# api doc location
http://127.0.0.1:8000/docs