# dependency
- `conda install numpy`
- `pip install keyboard`
- `conda install -c conda-forge pyautogui`
- `pip install fastapi`
- `pip install pillow`

# run server
uvicorn web_api:app

list all ports ps
`lsof -i:8000`
kill them
`kill -9 $(lsof -t -i:8000)`

# run client

`python worker_client.py screenshot`

`python worker_client.py keyboard`
