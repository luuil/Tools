from locust import HttpLocust, TaskSet, task

img_path = r'./data/0a1c7f1f548c4bd8de9aa3fe1d4c8ea1af60d279.jpeg'
img_url = r'http://screenshot.msstatic.com/yysnapshot/17115464e8eb8805a6998236915c826e9f3e5b763db5'

with open(img_path, 'rb') as f:
    img = f.read()


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("start..")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("done..")
    
    # @task
    # def check(self):
    #     self.client.get("/check")
    
    @task
    def pubg_map_file(self):
        self.client.post("/game/pubg_map", files={'file': img})
    
    @task
    def pubg_map_url(self):
        self.client.post("/game/pubg_map", {'url': img_url})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000