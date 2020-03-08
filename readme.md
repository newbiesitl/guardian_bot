# run server
uvicorn web_api:app

list all ports ps
`lsof -i:8000`
kill them
`kill -9 $(lsof -t -i:8000)`