import time

from pycore.utils import time_utils


class Agent(object):
    def __init__(self):
        self.id = 0
        self.create_date = time_utils.stamp_to_string(time.time(), "%Y-%m-%d")
        self.user_id = 0
        self.parent_id = 0
        self.parent_ids = ''
        self.top_id = 0
        self.min = 0
        self.total_min = 0
        self.status = 0
        self.contact = ''
