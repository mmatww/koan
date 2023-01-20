import boto3
import os

AWS_PROFILE = os.getenv("AWS_PROFILE", "default")

boto3.setup_default_session(profile_name=AWS_PROFILE)
resource = boto3.resource("iam")
client = boto3.client("iam")

for user in resource.users.all():
    metadata = client.list_access_keys(UserName=user.user_name)
    if metadata["AccessKeyMetadata"]:
        for key in user.access_keys.all():
            access_id = key.access_key_id
            status = key.status
            last_used = client.get_access_key_last_used(AccessKeyId=access_id)
            if (status == "Active"):
                status = "NEVER"
                if "LastUsedDate" in last_used["AccessKeyLastUsed"]:
                    status = str(last_used["AccessKeyLastUsed"]["LastUsedDate"])[:10]
            print(f"Key: {access_id}\tCreated: {str(key.create_date)[:10]}\tLast Used: {status.upper()}\tUser: {user.user_name}")
