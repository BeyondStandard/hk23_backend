## Running the Backend using Docker

* `docker build --no-cache -t myfastapiimage .
`
* `docker run --name myfastapiimage -it -v /Users/ashmi/Scripts/open-source/hackatum-2022/backend:/backend -p 8000:8000  myfastapiimage`

To start locally:

* `cd src/`
* `gunicorn -w 3 -k uvicorn.workers.UvicornWorker app.app:app --bind 0.0.0.0:8000`