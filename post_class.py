#Post class, creates object for each post to be passed to oracle database

from datetime import datetime


class Post:
    post_id = 0

    def __init__(self, user_id, data):
        self._id = Post.post_id + 1
        self._user_id = user_id
        self._time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._data = data
        Post.post_id += 1

    def __str__(self):
        return f"<Post ID{self._id}>"
    
    def get_id(self):
        return self._id
    def get_user_id(self):
        return self._user_id
    def get_time(self):
        return self._time
    def get_data(self):
        return self._data
    
    def set_data(self, data):
        self._data = data
