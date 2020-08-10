import boto3
from datetime import datetime, timezone


class StorageAPI:

    def __init__(self):
        self.instance = boto3.client('s3')
        self.resource = boto3.resource('s3')
        self.bucket = self.resource.Bucket(self.bucket_name)


    def upload(self, name, content, key=None):
        if not key:
            key = name

        obj = self.resource.Object(self.bucket_name, name)
        obj.put(Body=content, Bucket=self.bucket_name)

        self.instance.put_object(
            Bucket=self.bucket_name,
            Key=key,
        )


    def is_file_exists(self, target):
        objs = list(self.bucket.objects.filter(Prefix=target))
        return len(objs) > 0 and objs[0].key == target


    def is_timeout(self, target):
        for obj in self.bucket.objects.all():
            if obj.key != target: continue
            delta = (datetime.now(timezone.utc) - obj.last_modified)
            return delta.total_seconds() >= 60
        return True # default timeout if file not found or something


    @property
    def bucket_name(self):
        return 'datastax-storage'


Storage = StorageAPI()
