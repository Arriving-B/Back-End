import httpx

busColor = {
    # RED
    "광역" : "#F72F08",
    "직행좌석" : "#F72F08",

    # GREEN
    "지선" : "#5BB025",
    "맞춤" : "#5BB025",
    "마을" : "#5BB025",

    # BLUE
    "간선" : "#3D5BAB",
    "심야" : "#3D5BAB",
    "좌석" : "#3D5BAB",
    "일반" : "#3D5BAB",

    # YELLOW
    "순환" : "#F99D1C",
    "투어" : "#F99D1C",

    # BROWN
    "공항" : "#8B4513",

    # PURPLE
    "급행" : "#6E2DB9",

    # Another
    "BRT" : "#CB2B2B",
    "두루타" : "#00A0C6",
    "누비다" : "#FF69B4",
    "임시" : "#FFBC00",
    "행복" : "#FA5882",
    "읍면" : "#5FBF15",
    "마실" : "#FFBC00",
    "출근" : "#82D438",
    "군위" : "#002187",
    "폐선" : "#AAAAAA"
}

# GET Method
## 정류장의 버스 목록 조회
async def get_curSttnBusList(url: str):
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
                        "color": busColor.get(temp["routetp"][0:-2]),
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
                print(dataBundle)
                for temp in dataBundle["response"]["body"]["items"]["item"]:
                    for busData in data["data"]["bus_list"]:
                        if busData["bus_id"] == temp["routeid"]:
                            if busData["time_left"] == -1 or busData["time_left"] > temp["arrtime"]:
                                busData["station_left"] = temp["arrprevstationcnt"]
                                busData["time_left"] = temp["arrtime"]
                return data
        finally:
            return data
        