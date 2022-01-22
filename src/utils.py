import configparser
import motor.motor_asyncio

config = configparser.ConfigParser()
config.read("config.ini")
client = motor.motor_asyncio.AsyncIOMotorClient(config["DEFAULT"]["mongo_uri"])
db = client.clothingDB
