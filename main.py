from chat import afrohistorian

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Afrohistorian API"}

@app.post("/ask")
async def ask_afrohistorian(query: str):
    answer = afrohistorian(text=query)
    return answer

def main():
    name = input("What is your name?\n")
    print(f"Hello, {name}!")
    query = input("What do you want to know about African history?\n")
    answer = afrohistorian(text=query)
    print(f"Afrohistorian says: {answer['response']}")


if __name__ == "__main__":
    main()