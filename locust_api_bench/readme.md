# Locust API benchmark

Usage for [Locust](https://locust.io/), more details please check [quick start](https://docs.locust.io/en/stable/quickstart.html).

There is also an [docker image](https://github.com/zalando-incubator/docker-locust) available. For quick start, please refer to [docker_locust.sh](./docker_locust.sh).

## Usage

### Install

```
pip install locust
```

### Create `locustfile.py`

```
from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        self.client.post("/login", {"username":"ellen_key", "password":"education"})

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def profile(self):
        self.client.get("/profile")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
```

### Run in command line

```
locust -f ./locustfile.py --host=http://localhost:5000
```

> where `--host` is your API address, `http://localhost:5000` in our case.

### Run in docker

```bash
sudo docker run -i --rm \
    -v $PWD/reports:/opt/reports \
    -v ~/.aws:/root/.aws \
    -v $PWD/:/opt/script \
    -v $PWD/credentials:/meta/credentials \
    -p 8089:8089 \
    -e ROLE=standalone \
    -e TARGET_HOST=http://0.0.0.0:5000 \
    -e LOCUST_FILE=./wukong_pubg_bench.py \
    -e SLAVE_MUL=4 \
    -e AUTOMATIC=False \
    registry.opensource.zalan.do/tip/docker-locust
```

### Open from browser

Click or paste [http://localhost:8089](http://localhost:8089), and we can see `full` Locust, enjoy!