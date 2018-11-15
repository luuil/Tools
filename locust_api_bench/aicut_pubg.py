from locust import HttpLocust, TaskSet, task

img_path = r'./data/0a9f903250629668b743bf05f94ca262c4b0d508.jpeg'
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
    def post_local_file(self):
        response = self.client.post("/aicut/pubg", files={'file': img})
    

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 1000