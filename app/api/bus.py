import httpx

# GET Method
## 정류장의 버스 목록 조회
async def get_curSttnBusList(url: str, busColorData: dict):
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
                        "color": busColorData[temp["routetp"][0:-2]],
                        # -1 : 도착 정보 없음
                        "station_left": -1,
                        "time_left": -1
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
        
# GET Method
## 도착 예정 버스목록 조회
async def get_arvlBusList(url: str, data: dict):
    if data["status"] != 200: 
        return data
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                dataBundle = response.json()
                for temp in dataBundle["response"]["body"]["items"]["item"]:
                    for busData in data["data"]["bus_list"]:
                        if busData["bus_id"] == temp["routeid"]:
                            if busData["time_left"] == -1 or busData["time_left"] > temp["arrtime"]:
                                busData["station_left"] = temp["arrprevstationcnt"]
                                busData["time_left"] = temp["arrtime"]
                return data
        finally:
            return data

# GET Method
## 버스 조회
async def get_busByContext(url: str, busColorData: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                dataBundle = response.json()
                data = []
                for temp in dataBundle["response"]["body"]["items"]["item"]:
                    data.append({
                        "bus_id": temp["routeid"],
                        "num": temp["routeno"],
                        "type": temp["routetp"][0:-2],
                        "color": busColorData[temp["routetp"][0:-2]]
                    })
                return data
            return None
        except:
            return None