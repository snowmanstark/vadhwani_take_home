import os

import redis
from pymongo import MongoClient

from google.cloud import translate_v2 as translate


r = redis.Redis(host=os.environ.get("REDIS_HOST"), decode_responses=True)

mongo_user = "app_user" # os.environ.get("MONGO_ROOT_USER")
mongo_password = "test123" # os.environ.get("MONGO_ROOT_PASSWORD")
client = MongoClient("mongodb://%s:%s@db/?authSource=app_db&authMechanism=SCRAM-SHA-256" % (mongo_user, mongo_password))
db = client["project_db"]

tc = translate.Client.from_service_account_json('./service-account.json')

# Source languare for translation
src_lang = "en"
# Target language for translation
target_langs = ["hi", "mr", "te", "pa"]
# fonts = {"hi":"KrutiDev", "mr", "te", "pa"}