import common, asyncio, aiohttp, json



async def PLAYERDATA(id):
    if id is None: return None
    url = "https://pointercrate.com/api/v1/players/" + str(id)
    async with aiohttp.request("GET",url) as string:
        string = string[2:len(string) - 1]; string = string.replace("\\n",""); string = string.replace("  ","")
        data = json.loads(string)
        print(data['data'])
        return data['data']



