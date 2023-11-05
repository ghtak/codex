import os
import boto3
from botocore.config import Config
import dotenv


# def create_directory_if_not_exist(client, bucket, path):
#     try:
#         client.head_object(Bucket=bucket, Key=path)
#     except:
#         client.put_object(Bucket=bucket, Body='', Key=path)


# def create_directory(client, bucket, base_path, new_path):
#     create_directory_if_not_exist(client, bucket, base_path)
#     paths = [x for x in new_path.split('/') if len(x) > 0]
#     for p in paths:
#         base_path = os.path.join(base_path, p) + '/'
#         create_directory_if_not_exist(client, bucket, base_path)


# def dir_date(client, bucket, path):
#     try:
#         return client.head_object(Bucket=bucket, Key=path).get('LastModified')
#     except:
#         return datetime.datetime.now()

class S3AccessInfo:
    def __init__(self,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 region_name: str):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name


class S3Api:
    def __init__(self,
                 bucket: str,
                 base_path: str,
                 access_info: S3AccessInfo):
        self.bucket = bucket
        self.base_path = base_path
        self.client = boto3.client('s3',
                                   aws_access_key_id=access_info.aws_access_key_id,
                                   aws_secret_access_key=access_info.aws_secret_access_key,
                                   region_name=access_info.region_name,
                                   config=Config(signature_version='s3v4'))

    def exist(self, pathfile):
        try:
            self.client.head_object(
                Bucket=bucket, Key=os.path.join(self.base_path, pathfile))
            return True
        except:
            return False

    def ls(self, path, with_recursive=False):
        paginator = self.client.get_paginator('list_objects_v2')
        if with_recursive:
            iter = paginator.paginate(Bucket=self.bucket,
                                      Prefix=os.path.join(self.base_path, path))
        else:
            iter = paginator.paginate(Bucket=self.bucket,
                                      Prefix=os.path.join(
                                          self.base_path, path),
                                      Delimiter='/')
        for page in iter:
            for prefix in page.get('CommonPrefixes', []):
                key = prefix.get('Prefix')
                name = key.replace(self.base_path, '')
                if len(name) > 0:
                    yield {'type': 'D', 'key': key, 'name': name}
            for obj in page.get('Contents', []):
                key = obj.get('Key')
                name = key.replace(self.base_path, '')
                if len(name) > 0:
                    yield {'type': 'F', 'key': key, 'name': name,
                           'size': obj.get('Size'),
                           'last_modified': obj.get('LastModified')}

    def upload(self, filename, pathfile):
        try:
            self.client.upload_file(filename,
                                    self.bucket, os.path.join(self.base_path, pathfile))
        except Exception as s3e:
            raise s3e
            # raise S3ManipOpError(message=str(s3e))

    def mv(self, src, dst):
        try:
            src_key = os.path.join(self.base_path, src)
            dst_key = os.path.join(self.base_path, dst)
            copy_source = {'Bucket': self.bucket,
                           'Key': src_key}

            self.client.copy_object(Bucket=self.bucket,
                                    CopySource=copy_source, Key=dst_key)
            self.client.delete_object(Bucket=self.bucket, Key=src_key)
        except Exception as s3e:
            raise s3e

    def rm(self, pathfile):
        try:
            self.client.delete_object(
                Bucket=self.bucket, Key=os.path.join(self.base_path, pathfile))
        except Exception as s3e:
            raise s3e

    def rm_dir(self, path):
        for file in self.ls(path, with_recursive=True):
            self.rm(file.get('name'))


if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    bucket = 'hdg-prj'
    s3_api = S3Api(bucket=bucket,
                   base_path='',
                   # base_path='matilda-asset-hub-backend/',
                   # base_path='s3_repo/',
                   access_info=S3AccessInfo(
                       aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                       aws_secret_access_key=os.environ.get(
                           "AWS_SECRET_ACCESS_KEY"),
                       region_name=os.environ.get("REGION_NAME")))

    # for item in s3_api.ls("matilda-asset-hub-backend/dvc_repo/1/14/"):
    # for item in s3_api.ls("dvc_repo/1/", with_recursive=True):
    file_counts = 0
    for item in s3_api.ls("", with_recursive=True):
        file_counts += 1
    print(file_counts)

    # s3_api.rm_dir('1/')

    # print(s3_api.exist('dvc_repo/1/14/0d99de9216cdc9a819c47b35d95cab'))
    # s3_api = S3Api(client, bucket, "s3_merge")
