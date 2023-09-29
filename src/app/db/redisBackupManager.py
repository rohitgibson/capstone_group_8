import boto3 

client_addr = ""

class RedisBackupManager:
    def __init__(self):
        self.aws_conn = None