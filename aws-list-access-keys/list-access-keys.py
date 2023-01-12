import boto3
import os

AWS_PROFILE = os.getenv("AWS_PROFILE", "default")

boto3.setup_default_session(profile_name=AWS_PROFILE)
resource = boto3.resource("iam")
client = boto3.client("iam")

for user in resource.users.all():
    Metadata = client.list_access_keys(UserName=user.user_name)
    if Metadata["AccessKeyMetadata"]:
        for key in user.access_keys.all():
            AccessId = key.access_key_id
            Status = key.status
            LastUsed = client.get_access_key_last_used(AccessKeyId=AccessId)
            status = "INACTIVE"
            if (Status == "Active"):
                status = "NEVER"
                if "LastUsedDate" in LastUsed["AccessKeyLastUsed"]:
                    status = str(LastUsed["AccessKeyLastUsed"]["LastUsedDate"])[:10]
            print(f"Key: {AccessId}\tCreated: {str(key.create_date)[:10]}\tLast Used: {status}\tUser: {user.user_name}")
