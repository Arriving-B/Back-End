import httpx

# GET Method
async def get_route(url: str, cityCodeUrl: str, cityCode: int, busColorData: dict):
    async with httpx.AsyncClient() as client:
        try:
            cityList = (await client.get(cityCodeUrl)).json()["response"]["body"]["items"]
            for temp in cityList["item"]:
                if temp["citycode"] == cityCode:
                    city = temp["cityname"]
            response = await client.get(url)
            if response.status_code == 200:
                dataBundle = response.json()
                data = dataBundle["response"]["body"]["items"]["item"]
                return {
                    "status": 200,
                    "message": "Route inquiry successful",
                    "data": {
                        "bus_id": data["routeid"],
                        "city": city,
                        "num": data["routeno"],
                        "type": data["routetp"][0:-2],
                        "color": busColorData[data["routetp"][0:-2]],
                        "ep_nm": data["endnodenm"],
                        "sp_nm": data["startnodenm"],
                        "fd_time": str(data["startvehicletime"]),
                        "ld_time": str(data["endvehicletime"]),
                        "interval_time": data["intervaltime"],
                        "interval_haltime": data["intervalsuntime"]
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
            
        