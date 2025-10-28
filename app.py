import air
import os
import json
from air import Air
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Air()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


class PromptifyRequest(BaseModel):
    text: str
    prompt: str


async def generate_stream(text: str, prompt_template: str):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            yield f"data: {json.dumps({'error': 'GEMINI_API_KEY not configured'})}\n\n"
            return

        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash-exp")
        model = genai.GenerativeModel(model_name)

        filled_prompt = prompt_template.replace("{text}", text)
        response = model.generate_content(filled_prompt, stream=True)

        for chunk in response:
            if chunk.text:
                yield f"data: {json.dumps({'chunk': chunk.text})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': f'Gemini API failed: {str(e)}'})}\n\n"


@app.post("/api/promptify")
async def promptify(request: PromptifyRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail={"error": "Input text cannot be empty."})

    return StreamingResponse(
        generate_stream(request.text, request.prompt),
        media_type="text/event-stream"
    )


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
                        air.Button(
                            "📋 Copy",
                            id="copy-btn",
                            **{"class": "outline"},
                            style="padding: 0.5rem 1rem;",
                        ),
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
            air.Div(
                air.Button(
                    "✨ Promptify",
                    id="promptify-btn",
                    **{"class": "primary"},
                    style="padding: 0.75rem 2rem; font-size: 1.1rem; font-weight: 600; cursor: pointer;",
                ),
                style="display: flex; justify-content: center; margin: 2rem 0;",
            ),
            air.Main(
                air.H1("Hello World"),
            ),
            air.Script("""
document.getElementById('copy-btn').addEventListener('click', function() {
    const outputText = document.getElementById('output-text');
    const btn = this;
    const originalText = btn.innerHTML;

    navigator.clipboard.writeText(outputText.value).then(() => {
        btn.innerHTML = '✓ Copied';
        btn.disabled = true;
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2000);
    });
});
            """),
        ),
    )
