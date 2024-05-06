import httpx

busColor = {
    # RED
    "광역" : "#F72F08",
    "직행" : "#F72F08",

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
                        "color": busColor.get(temp["routetp"][0:-2]),
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
        