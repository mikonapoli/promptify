import air
from air import Air

app = Air()


@app.get("/")
def home():
    return air.Html(
        air.Head(
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Title("Promptify"),
            air.Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            air.Link(rel="preconnect", href="https://fonts.googleapis.com"),
            air.Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="anonymous"),
            air.Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"),
        ),
        air.Body(
            air.Main(
                air.H1("Hello World"),
            ),
        ),
    )
