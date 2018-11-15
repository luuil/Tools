# docker run -i --rm \
# -v $PWD/reports:/opt/reports \
# -v ~/.aws:/root/.aws \
# -v $PWD/:/opt/script \
# -v $PWD/credentials:/meta/credentials \
# -p 8089:8089 \
# -e ROLE=standalone \
# -e TARGET_HOST=https://localhost:5200 \
# -e LOCUST_FILE=https://raw.githubusercontent.com/zalando-incubator/docker-locust/master/example/simple.py \
# -e SLAVE_MUL=4 \
# -e AUTOMATIC=False \
# registry.opensource.zalan.do/tip/docker-locust

from locust import HttpLocust, TaskSet, task

def readfile(p):
    with open(p, 'rb') as f:
        img = f.read()
        return img


p_audio = '/data/audio/sing (1).wav'
p_blzy = '/data/blzy/48_2.png'
p_cjzc = '/data/cjzc/26_2.jpeg'
p_food = '/data/food/food1.jpg'
p_gok = '/data/gok/0be406ca7755c83025c97cc8ee3c102bd04e428d.jpeg'
p_lol = '/data/lol/1709a2aa67fb0d20f0c8a555ec092d77520dee2c30b5.jpg'
p_nsh = '/data/nsh/jiuling.png'
p_pubg = '/data/pubg/0a17b87b6ec5ade9581fa84b17cdb624d36ff6bb.jpeg'
p_qjcj = '/data/qjcj/37_4.jpeg'
p_qrcode = '/data/qrcode/1.png'
p_xingxiu = '/data/xingxiu/2.jpeg'
p_yanzhi = '/data/yanzhi/dance.jpeg'


raw_audio = readfile(p_audio)
raw_blzy = readfile(p_blzy)
raw_cjzc = readfile(p_cjzc)
raw_food = readfile(p_food)
raw_gok = readfile(p_gok)
raw_lol = readfile(p_lol)
raw_nsh = readfile(p_nsh)
raw_pubg = readfile(p_pubg)
raw_qjcj = readfile(p_qjcj)
raw_qrcode = readfile(p_qrcode)
raw_xingxiu = readfile(p_xingxiu)
raw_yanzhi = readfile(p_yanzhi)




class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("start..")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("done..")
    
    
    @task(1)
    def audio(self):
        data = {"contents": "all", "dtype": "image", "pid": 911}
        response = self.client.post("/audio", data=data, files={'file': raw_audio})
        print("{}: {}".format(response.status_code, response.text))

    
    @task(15)
    def blzy(self):
        data = {"contents": "digit", "dtype": "image", "pid": 911}
        response = self.client.post("/blzy", data=data, files={'file': raw_blzy})
        print("{}: {}".format(response.status_code, response.text))

    
    @task(150)
    def cjzc(self):
        data = {"contents": "digit,state", "dtype": "image", "pid": 911}
        response = self.client.post("/cjzc", data=data, files={'file': raw_cjzc})
        print("{}: {}".format(response.status_code, response.text))

    
    # @task
    # def food(self):
    #     response = self.client.post("/food", data=data, files={'file': raw_food})
    #     print("{}: {}".format(response.status_code, response.text))

    
    @task(260)
    def gok(self):
        data = {"contents": "digit,hero", "dtype": "image", "pid": 911}
        response = self.client.post("/gok", data=data, files={'file': raw_gok})
        print("{}: {}".format(response.status_code, response.text))

    
    @task(15)
    def lol(self):
        data = {"contents": "hero", "dtype": "image", "pid": 911}
        response = self.client.post("/lol", data=data, files={'file': raw_lol})
        print("{}: {}".format(response.status_code, response.text))

    
    @task(20)
    def nsh(self):
        data = {"contents": "hero", "dtype": "image", "pid": 911}
        response = self.client.post("/nsh", data=data, files={'file': raw_nsh})
        print("{}: {}".format(response.status_code, response.text))

    
    # @task
    @task(150)
    def pubg(self):
        data = {"contents": "digit,state", "dtype": "image", "pid": 911}
        response = self.client.post("/pubg", data=data, files={'file': raw_pubg})
        print("{}: {}".format(response.status_code, response.text))

    
    @task(20)
    def qjcj(self):
        data = {"contents": "digit,state", "dtype": "image", "pid": 911}
        response = self.client.post("/qjcj", data=data, files={'file': raw_qjcj})
        print("{}: {}".format(response.status_code, response.text))
    
    @task(150)
    def qrcode(self):
        data = {"contents": "qrcode", "dtype": "image", "pid": 911}
        response = self.client.post("/qrcode", data=data, files={'file': raw_qrcode})
        print("{}: {}".format(response.status_code, response.text))

    
    @task(330)
    def xingxiu(self):
        data = {"contents": "dance", "dtype": "image", "pid": 911}
        response = self.client.post("/xingxiu", data=data, files={'file': raw_xingxiu})
        print("{}: {}".format(response.status_code, response.text))

    
    @task(100)
    def yanzhi(self):
        data = {"contents": "dance", "dtype": "image", "pid": 911}
        response = self.client.post("/yanzhi", data=data, files={'file': raw_yanzhi})
        print("{}: {}".format(response.status_code, response.text))



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 1000