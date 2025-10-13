from fastapi import FastAPI


app = FastAPI()


# Route - combination of the http method and path
@app.get("/home")
async def home():
    return {"Hello World!"}
