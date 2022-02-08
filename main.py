from sre_constants import SUCCESS
from xmlrpc.client import boolean
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum

import boto3, json, os

os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cuisine')

app = FastAPI()

class Dish(BaseModel):
    is_deleted: boolean
    genre: str
    name: str

# 料理一覧を取得する
@app.get("/dish")
async def get_dish():
    result = table.scan()
    return result['Items']

# 主菜一覧を取得する
@app.get("/dish/main")
async def get_main_dish():
    result = table.scan()
    return result['Items']

# 副菜一覧を取得する
@app.get("/dish/side")
async def get_side_dish():
    result = table.scan()
    return result['Items']

# 料理を登録する
@app.post("/dish")
async def add_dish(dish: Dish):
    response = table.put_item(
        Item = {
            'isDeleted': dish.is_deleted,
            'genre': dish.genre,
            'name': dish.name
        }
    )
    return SUCCESS

handler = Mangum(app, spec_version=2)
