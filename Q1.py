from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# GET Method
@app.get("/api/test")
async def get_test():
    return "Hello World"

# 定義請求體模型
class TestRequest(BaseModel):
    key: str

# POST Method
@app.post("/api/test")
async def post_test(request: TestRequest):
    if request.key == "cxcxc":
        return "Succeeded"
    return "Failed"

# 如果要直接運行這個檔案
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)