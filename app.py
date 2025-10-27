from air import Air

app = Air()


@app.get("/")
def home():
    return "Hello World"
