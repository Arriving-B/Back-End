import httpx

# GET Method
async def get_station(url: str, skip: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                dataBundle = response.json()

                # 정류장 없음
                if dataBundle["response"]["body"]["totalCount"] <= skip:
                    return {
                        "status": 204,
                        "message": "Station not found"
                    }
                
                # 정류장 있음
                data = dataBundle["response"]["body"]["items"]["item"][skip]
                return {
                    "status": 200,
                    "message": "Station inquiry successful",
                    "data": {
                        "station_id": data["nodeid"],
                        "name": data["nodenm"],
                        "city_code": data["citycode"],
                        "latitude": data["gpslati"],
                        "longitude": data["gpslong"]
                    }
                }
            else:
                # OpenAPI로 부터 지정되지 않은 응답 수신
                return {
                    "status": 502,
                    "message": "Open API server is gone"
                }
        except:
            # 예외처리
            return {
                "status": 404,
                "message": "Not found"
            }
            
# GET Method
## 정류장 조회
async def get_stationByContext(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                dataBundle = response.json()
                data = []
                for temp in dataBundle["response"]["body"]["items"]["item"]:
                    data.append({
                        "station_id": temp["nodeid"],
                        "name": temp["nodenm"],
                        "latitude": temp["gpslati"],
                        "longitude": temp["gpslong"]
                    })
                return data
            return None
        except:
            return None