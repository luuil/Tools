# https://github.com/zalando-incubator/docker-locust
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