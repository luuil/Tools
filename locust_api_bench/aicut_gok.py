from locust import HttpLocust, TaskSet, task

img_path = r'./data/gok/0aafe877505919bb0ab8a7d70087c174f02cc1b5.jpeg'

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
        response = self.client.post("/aicut/gok", files={'file': img})
    

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 1000
