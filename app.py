import air
import os
import json
from air import Air
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, RedirectResponse
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


def render_app():
    return air.Html(
        air.Head(
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Title("Promptify"),
            air.Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            air.Link(rel="preconnect", href="https://fonts.googleapis.com"),
            air.Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="anonymous"),
            air.Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"),
            air.Style("""
                * { font-family: 'Inter', sans-serif; }
                body {
                    min-height: 100vh;
                    background: linear-gradient(to bottom, #f8fafc, #f1e5ff);
                    margin: 0;
                    padding: 1rem;
                }
                @media (min-width: 768px) {
                    .panels-grid { grid-template-columns: 1fr 1fr !important; }
                }
            """),
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
                        air.Button(
                            "🎤 Dictate",
                            id="mic-btn",
                            **{"class": "outline"},
                            style="padding: 0.5rem 1rem;",
                        ),
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
            air.Div(
                id="error-banner",
                style="display: none; background: #fee; color: #c00; padding: 1rem; margin: 1rem 0; border-radius: 8px; text-align: center;",
            ),
            air.Main(
                air.H1("Hello World"),
            ),
            air.Script("""
let recognition = null;
let isListening = false;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onresult = function(event) {
        const inputText = document.getElementById('input-text');
        for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                inputText.value += event.results[i][0].transcript + ' ';
            }
        }
    };

    recognition.onerror = function() {
        stopDictation();
    };

    recognition.onend = function() {
        if (isListening) {
            isListening = false;
            const btn = document.getElementById('mic-btn');
            btn.innerHTML = '🎤 Dictate';
            btn.style.background = '';
            btn.style.color = '';
        }
    };
}

function startDictation() {
    if (!recognition) return;
    recognition.start();
    isListening = true;
    const btn = document.getElementById('mic-btn');
    btn.innerHTML = '🔴 Stop';
    btn.style.background = '#dc2626';
    btn.style.color = 'white';
}

function stopDictation() {
    if (!recognition) return;
    recognition.stop();
    isListening = false;
    const btn = document.getElementById('mic-btn');
    btn.innerHTML = '🎤 Dictate';
    btn.style.background = '';
    btn.style.color = '';
}

document.getElementById('mic-btn').addEventListener('click', function() {
    if (!recognition) {
        alert('Speech recognition not supported in this browser');
        return;
    }
    if (isListening) stopDictation();
    else startDictation();
});

const PROMPT_TEMPLATE = `<input>
{text}
</input>

You are an expert prompt engineer. Your task is to rewrite the user's request in <input /> as a detailed and precise prompt for an AI model.

1. Read <input /> carefully and make sure you understand the user's request in its entirety and with full context and details.
2. Plan carefully how to rewrite the request as a detailed and precise prompt for an AI model. Consider what specific information, instructions, or context the AI model would need to fulfill the user's request effectively.
3. Rewrite the user's request as a detailed and precise prompt for an AI model, ensuring clarity, specificity, and completeness. The prompt should guide the AI model to produce the desired output without ambiguity.
  - Use clear and specific language. Think of this as language as specification / code, not natural language.
  - Use headings (##, ###, ####) where appropriate. No need for a first-level title or heading, only for sections (and only where it's called for).
  - Use **bold**, _italics_, bullet points ( - , not * ), and numbered lists ( 1. , 2. ) liberally to organize the prompt effectively. Never use emojis.
  - Always start with a single short paragraph summarising and describing the overall task.
  - The resulting prompt should be concise and specific, avoiding unnecessary complexity or verbosity. It should be at most 1.5X the length of the original request in <input />, and at least 0.75X of the length of the original request in <input />.
  - Use plain, straightforward, precise language without embellishments, niceties, or creative flourishes.
  - Do not add or invent any information that is not present in <input />.
  - Output the final prompt only, as markdown, without any additional commentary or explanation.`;

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

function showError(message) {
    const banner = document.getElementById('error-banner');
    banner.textContent = message;
    banner.style.display = 'block';
}

function hideError() {
    const banner = document.getElementById('error-banner');
    banner.style.display = 'none';
}

document.getElementById('promptify-btn').addEventListener('click', async function() {
    const inputText = document.getElementById('input-text').value;
    const outputText = document.getElementById('output-text');
    const btn = this;
    const originalText = btn.innerHTML;

    if (!inputText.trim()) {
        showError('Input text cannot be empty.');
        return;
    }

    hideError();
    outputText.value = '';
    btn.disabled = true;
    btn.innerHTML = '⏳ Prompt engineer is working...';

    try {
        const response = await fetch('/api/promptify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText, prompt: PROMPT_TEMPLATE })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const {value, done} = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.chunk) outputText.value += data.chunk;
                    if (data.error) {
                        showError(data.error);
                        return;
                    }
                    if (data.done) break;
                }
            }
        }
    } catch (e) {
        showError('Failed to connect to server: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
});
            """),
        ),
    )


@app.get("/")
def root():
    return RedirectResponse(url="/promptify", status_code=307)


@app.get("/promptify")
def promptify_home():
    return render_app()
