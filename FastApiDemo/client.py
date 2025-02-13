# client.py
import httpx

json_data ={
    "admin":ozge,
    "password":1234
}

http = httpx.AsyncClient(base_url="http://127.0.0.1:8000")

class Client:
    async def post_json_data(self):
        url= "/process-json"
        
        try:
            response = await http.post(url, json=json_data)
            return response.json()
        except Exception as e :
            print(e)
        return {}


# response = httpx.post("http://localhost:27017/process-json/", json=json_data)

# print(response.json())
