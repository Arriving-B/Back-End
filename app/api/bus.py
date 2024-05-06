import httpx

# GET Method
async def get_busList(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                dataBundle = response.json()
                data = []
                for temp in dataBundle["response"]["body"]["items"]["item"]:
                    data.append({
                        "bus_id": temp["routeid"],
                        "name": temp["routeno"],
                        "type": temp["routetp"][0:-2],
                        "color": "#aaffaa",
                        "station_left": temp["arrprevstationcnt"],
                        "time_left": temp["arrtime"]
                    })
                return {
                    "status": 200,
                    "message": "Bus inquiry successful",
                    "data": {
                        "bus_list": data
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
                "message": "Bus not found"
            }
        