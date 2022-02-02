from flask import Flask, request, jsonify
import asyncio
import aiohttp
import os
import requests
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils import *
from waitress import serve

BASE_URL = "https://kolayik.com/api/v2/"
LIST_URL = "https://kolayik.com/api/v2/person/list?status={}&page={}"
VIEW_URL = "https://kolayik.com/api/v2/person/view/{}"


def get_tasks(session, header, symbols, status):
    tasks = []
    for symbol in symbols:
        tasks.append(asyncio.create_task(session.post(LIST_URL.format(str(status), str(symbol)), ssl=False, headers=header)))
    return tasks

async def get_symbols(header,symbols, results, status):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, header,symbols, status)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            temp = await response.json()
            for i in temp['data']['items']:
                results.append(i['id'])

def get_people_tasks(session, header, person_id_list):
    tasks = []
    for person in person_id_list:
        tasks.append(asyncio.create_task(session.get(VIEW_URL.format(person), ssl=False, headers=header)))
    return tasks

async def get_people(header, results, people_list):
    async with aiohttp.ClientSession() as session:
        tasks = get_people_tasks(session, header, results)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            temp = await response.json()
            person = temp['data']['person']
            people_list.append(person)

            # if temp['data']['person']['dataList'] != None:
            #     for y in temp['data']['person']['dataList']:
            #         if y['fieldToken'] == "meyerEntegrasyon":
            #             person['meyer'] = y['value']
            # if "meyer" in person['dataList'] and person['meyer'] == "Entegrasyon Yapılsın":
            #     people_list.append(person)


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['JSON_SORT_KEYS'] = False
limiter = Limiter(app, key_func=get_remote_address)

@limiter.limit("10/minute")
@app.route('/people', methods=['GET'])
def people():
    # print(request.headers.get("Authorization"))
    results = []
    people_list = []
    page_count = request.args.get("page_count")
    status = request.args.get("status")
    # print(path, page_count)
    # print(make_request("POST", LIST_URL, {"status":1, "page":1}, HEADER = dict(Authorization=request.headers.get("Authorization"))))
    symbols = list(range(1, int(page_count) + 1)) if int(page_count) != 1 else ["1"]
    header = dict(Authorization=request.headers.get("Authorization"))
    asyncio.run(get_symbols(header, symbols, results, status))
    asyncio.run(get_people(header, results, people_list))
    # print(len(people_list))
    return jsonify(people_list)


@app.route('/leaves', methods=['GET'])
def leaves():
    return(make_request("GET", "https://kolayik.com/api/v2/leave/list?status="+request.args.get("status")+"&startDate="+str(request.args.get("start_date"))+"&endDate="+str(request.args.get("end_date"))+"&limit=10000000",{},dict(Authorization=request.headers.get("Authorization"))))

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=port)