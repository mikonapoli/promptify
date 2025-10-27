import air
from air import Air
from fastapi.staticfiles import StaticFiles

app = Air()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


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
            air.Header(
                air.Div(
                    air.Img(src="/assets/promptify_logo.png", alt="Promptify Logo", style="height: 40px;"),
                    air.Span("|", style="margin: 0 1rem; color: #ccc;"),
                    air.Span("Promptify", style="font-weight: 600;"),
                    style="display: flex; align-items: center;",
                ),
            ),
            air.P(
                "Turn your ramblings into perfectly structured prompts.",
                style="text-align: center; margin: 2rem 0;",
            ),
            air.Div(
                air.Div(
                    air.Div(
                        air.H3("Your Ramblings", style="margin: 0 0 1rem 0;"),
                        style="display: flex; justify-content: space-between; align-items: center;",
                    ),
                    air.Textarea(
                        id="input-text",
                        placeholder="Paste or dictate your ramblings here...",
                        style="width: 100%; min-height: 300px; resize: none; background: #f5f5f5; border: 1px solid #ddd; border-radius: 4px; padding: 0.75rem;",
                    ),
                    **{"class": "panel-card"},
                    style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; flex-direction: column;",
                ),
                air.Div(
                    air.Div(
                        air.H3("Structured Prompt", style="margin: 0 0 1rem 0;"),
                        style="display: flex; justify-content: space-between; align-items: center;",
                    ),
                    air.Textarea(
                        id="output-text",
                        placeholder="Your structured prompt will appear here...",
                        readonly=True,
                        style="width: 100%; min-height: 300px; resize: none; background: #f5f5f5; border: 1px solid #ddd; border-radius: 4px; padding: 0.75rem;",
                    ),
                    **{"class": "panel-card"},
                    style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; flex-direction: column;",
                ),
                **{"class": "panels-grid"},
                style="display: grid; grid-template-columns: 1fr; gap: 1.5rem; margin: 2rem 0; min-height: 50vh;",
            ),
            air.Main(
                air.H1("Hello World"),
            ),
        ),
    )
