import json
import asyncio
import aiohttp
import time

ELASIC_URL = "https://soosdata.link:8222"
start_time = time.time()


async def get_elastic_data(session, url, data: dict, freq: str):
    try:
        async with session.post(url, json=data) as response:
            resp = json.loads(await response.read())
            if response.status != 200:
                return {"error": f"server returned {response.status}"}
            resp = resp["body"]["hits"]["hits"]
            if len(resp) > 0:
                res = [
                    {
                        "machine": v["_source"]["machine"],
                        "sensor": v["_source"]["sensor"],
                        "tfs": v["_source"]["tfs"],
                        freq: v["_source"]["value"][freq]
                    }
                    for v in resp if "_source" in v and freq in v['_source']['value']]
                return res

    except asyncio.TimeoutError:
        return {"results": f"timeout error on {data}"}


async def searchAsync(json_requests, freq):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for json_body in json_requests:
            tasks.append(asyncio.ensure_future(
                get_elastic_data(session, url=ELASIC_URL, data=json_body, freq=freq)))
        all_data = await asyncio.gather(*tasks)
        return all_data


def search(json_requests, freq='527'):
    '''

    :param json_requests:
    :param freq:
    :return:
    '''
    all_data = asyncio.run(searchAsync(json_requests, freq))
    return all_data
