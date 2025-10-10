# Promptify Product Specification

## 1. Overview
- **Purpose**: Provide a web experience that converts free-form user ramblings into structured, actionable prompts suitable for large language models.
- **Access Model**: Anonymous, single-user workflow. No authentication, accounts, or persistence.
- **Routing**: Application rooted at `/promptify`; all root traffic `/` redirects to this base path.

## 2. Core Workflows
- **Draft Input**: User types or dictates text into the primary textarea labelled `Your Ramblings`. Changes are instantly reflected; original formatting is preserved.
- **Prompt Generation**:
  1. User triggers the `Promptify` button.
  2. Client validates non-empty input, clears previous output and error state, and sends a new generation request.
  3. Structured prompt streams back into the output textarea in real time until completion or error.
- **Editing Output**: User can modify the streamed output manually at any time; subsequent streamed chunks append after existing content.
- **Copy Final Prompt**: Copy button writes the entire output textarea contents to the clipboard and confirms success via temporary icon change.
- **Error Handling**: Any validation or generation failure displays a single error banner, stops loading state, and leaves partial output visible for review.

## 3. Interface Specification
### 3.1 Global Layout & Styling
- Full-height page with light gradient background (`slate` to `purple`) and Inter font.
- Content housed in a centered container with responsive padding (mobile to desktop).
- All transitions use smooth 150 ms animations; focus styles clearly visible.

### 3.2 Header Bar
- Left-aligned brand row containing:
  - Logo sourced from `assets/promptify_logo.png`.
  - Vertical divider.
  - Title text `Promptify`.
- Header spans full width, uses light gradient background, subtle shadow, and bottom border.

### 3.3 Hero Messaging
- Centered paragraph under header:
  - Primary promise: “Turn your ramblings into perfectly structured prompts.”

### 3.4 Dual Panels
- Grid layout: single column on narrow viewports, two columns on medium and larger screens; minimum combined height equals half the viewport.
- Each panel is a white card with rounded corners, light gray border, shadow, and internal padding.
- Header row shows the panel title and optional action buttons (microphone or copy).
- Textareas:
  - Stretch to fill remaining vertical space; no resize handles.
  - Light gray background, darker text, purple focus ring.
  - Placeholder text displayed when empty.

#### 3.4.1 `Your Ramblings` Panel
- Placeholder: `Paste or dictate your ramblings here...`.
- Microphone toggle button:
  - Idle: white background, purple border and icon, hover tint.
  - Active: solid red background, white icon, pulsing animation.
  - Tooltip text switches between “Start Dictation” and “Stop Dictation”.

#### 3.4.2 `Structured Prompt` Panel
- Placeholder: `Your structured prompt will appear here...`.
- Copy button:
  - Default: white background, purple border and icon.
  - Disabled when output empty or immediately after copying.
  - On success, icon changes to checkmark for 2 seconds, then reverts.

### 3.5 Primary Action Button
- Centered beneath the panels.
- Label: `Promptify` with leading sparkle icon.
- Disabled states: when input textarea is empty or while a request is in flight.
- Loading state: text switches to `Prompt engineer is working...` with animated spinner; button remains disabled until completion or failure.

### 3.6 Feedback Elements
- **Loading**: Represented solely by the primary button’s spinner and text change.
- **Error Banner**: Appears below the panel grid when errors occur; red text on light red background, centered, rounded border.
- **Copy Confirmation**: Icon swap on the copy button acts as the only success signal.
- **Dictation Errors**: No visible banner; dictation simply stops.

## 4. Voice Dictation
- Uses the browser Speech Recognition API in continuous mode.
- If unavailable, microphone interactions have no effect but do not surface errors.
- Only finalised transcripts append to the input textarea, with a trailing space.
- Recognition errors automatically stop dictation and reset the listening flag.
- Microphone permission must be declared so the host platform prompts the user appropriately.

## 5. Prompt Generation Contract
- **Client Request**:
  - Rejects empty or whitespace-only input locally and surfaces “Input text cannot be empty.”.
  - Computes API base path from the first segment of the current location pathname; if present, prefixes all requests with `/<segment>`, otherwise uses root.
  - Sends `POST <base>/api/promptify` with JSON body `{ "text": "<user input>", "prompt": "<template>" }`.
- **Server Processing**:
  - Validates `text` and `prompt` presence, type `string`, and non-empty trimmed `text`; otherwise returns HTTP `400` with `{ "error": "<reason>" }`.
  - Replaces `{text}` placeholder in the template before forwarding to the AI model.
- **Streaming Response**:
  - Uses Server-Sent Events; each payload line starts with `data: ` followed by JSON.
  - `{ "chunk": "<string>" }`: client appends to output textarea.
  - `{ "error": "<message>" }`: client displays message, stops loading state, retains partial output.
  - `{ "done": true }`: marks successful completion and resets loading state.
- **Error Handling**:
  - Upstream AI failures emit `{ "error": "Gemini API failed: <message>" }` via SSE, then close the stream.
  - If the stream cannot start, server responds with HTTP `500` and JSON `{ "error": "The AI service failed", "message": "<detail>" }`.

## 6. Prompt Template
````markdown
<input>
{text}
</input>

You are an expert prompt engineer. Your task is to rewrite the user’s request in <input /> as a detailed and precise prompt for an AI model.

1. Read <input /> carefully and make sure you understand the user’s request in its entirety and with full context and details.
2. Plan carefully how to rewrite the request as a detailed and precise prompt for an AI model. Consider what specific information, instructions, or context the AI model would need to fulfill the user’s request effectively.
3. Rewrite the user’s request as a detailed and precise prompt for an AI model, ensuring clarity, specificity, and completeness. The prompt should guide the AI model to produce the desired output without ambiguity.
  - Use clear and specific language. Think of this as language as specification / code, not natural language.
  - Use headings (##, ###, ####) where appropriate. No need for a first-level title or heading, only for sections (and only where it’s called for).
  - Use **bold**, _italics_, bullet points ( - , not * ), and numbered lists ( 1. , 2. ) liberally to organize the prompt effectively. Never use emojis.
  - Always start with a single short paragraph summarising and describing the overall task.
  - The resulting prompt should be concise and specific, avoiding unnecessary complexity or verbosity. It should be at most 1.5X the length of the original request in <input />, and at least 0.75X of the length of the original request in <input />.
  - Use plain, straightforward, precise language without embellishments, niceties, or creative flourishes.
  - Do not add or invent any information that is not present in <input />.
  - Output the final prompt only, as markdown, without any additional commentary or explanation.
````
- Template must remain verbatim, including indentation and fenced code block, to ensure consistent behaviour.

## 7. Backend Behaviour
- **API Keys**:
  - Service fails fast if `GEMINI_API_KEY` environment variables are set or non-empty.
- **Model Selection**: Optional `GEMINI_MODEL_NAME` overrides default model identifier `gemini-2.5-pro`.
- **Logging**: Record request identifiers and duration for each generation call; log upstream errors with context.

## 8. Static Delivery & Routing
- Serve built assets from `/promptify`; handle client-side routing by returning the main HTML shell for any path under this base.
- Redirect root `/` to `/promptify`.
- Include Inter font and equivalent styling resources to replicate the specified typography and visual design.

## 9. Privacy & Security Considerations
- No persistence of user input or generated output; data exists only within the lifetime of the request/response cycle.
- Communicate privacy assurance in the hero message as specified.
- Keep all API keys confined to backend configuration; never expose them to client-side code or responses.
- Clipboard interactions rely on user gesture context (copy button) and standard permission prompts.

## 10. Accessibility
- Maintain contrast ratios for text, buttons, and error states to satisfy accessibility guidelines.
- Provide descriptive labels or tooltips for microphone, copy, and loading states; ensure the loading text is announced via `aria-live` or equivalent.
- Textareas must have discernible titles in the DOM to support screen readers.
- Keyboard navigation must reach all interactive elements, with visible focus indicators.

