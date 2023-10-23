from time import sleep

from redis import Redis

from boto3 import session

class RedisRestore:
    def __init__(self) -> None:
        self.restore_conn = Redis()

    def healthCheck(self):
        while True:
          current_redis_keys = self.checkDbKeys()
          pull_current_snapshot = self.pullCloudSnapshot()

    def checkDbKeys(self):
        try:
            list_redis_keys = self.restore_conn.keys(pattern='*address*')
        except Exception as e:
            print("An error was encountered while attempting to pull Redis keys:", e)
            return []
        
        return list_redis_keys

    def pullCloudSnapshot(self):
        pass