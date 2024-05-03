import httpx

# GET Method
async def get_station(url: str, skip: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                dataBundle = response.json()
                data = dataBundle["response"]["body"]["items"]["item"][skip]
                return {
                    "status": 200,
                    "message": "Station inquiry successful",
                    "data": {
                        "station_id": data["nodeid"],
                        "name": data["nodenm"]
                    }
                }
            else:
                return {
                    "status": 502,
                    "message": "Open API server is gone"
                }
        except:
            return {
                "status": 404,
                "message": "Station not found"
            }
        