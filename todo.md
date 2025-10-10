# Promptify Implementation Plan

## Vertical Slices (Thin Increments)

### Step 1: Basic Air App Setup
**What**: Install Air framework and create minimal FastAPI app that serves "Hello World"
**Acceptance**: Run `fastapi dev` and see "Hello World" at `http://localhost:8000`

### Step 2: Add PicoCSS and Base Layout
**What**: Include PicoCSS via CDN, add Inter font, create basic HTML structure with Air layout
**Acceptance**: Page displays with PicoCSS styling and Inter font applied

### Step 3: Implement Header with Logo and Title
**What**: Create header bar with logo image, divider, and "Promptify" title using Air tags
**Acceptance**: Header displays at top with logo (from assets/), divider, and title text

### Step 4: Add Hero Message
**What**: Insert centered paragraph below header with "Turn your ramblings into perfectly structured prompts."
**Acceptance**: Hero text displays centered below header

### Step 5: Create Dual Panel Layout Structure
**What**: Build responsive grid with two white card containers (empty for now)
**Acceptance**: Two side-by-side cards on desktop, stacked on mobile

### Step 6: Add Input Textarea Panel
**What**: First panel titled "Your Ramblings" with textarea and placeholder text
**Acceptance**: Left panel shows title, textarea accepts input, placeholder visible when empty

### Step 7: Add Output Textarea Panel
**What**: Second panel titled "Structured Prompt" with read-only textarea and placeholder
**Acceptance**: Right panel shows title, textarea displays, placeholder visible when empty

### Step 8: Add Promptify Button (UI Only)
**What**: Centered button below panels with sparkle icon and "Promptify" label, disabled when input empty
**Acceptance**: Button displays, disabled state works based on input textarea content

### Step 9: Add Copy Button (UI + Functionality)
**What**: Copy button in output panel header that writes textarea content to clipboard
**Acceptance**: Clicking copy button copies output text, icon changes to checkmark for 2s

### Step 10: Setup API Endpoint Structure
**What**: Create `/api/promptify` POST endpoint that validates input and returns mock response
**Acceptance**: POST to endpoint with `{"text": "test"}` returns success response

### Step 11: Integrate Gemini API Backend
**What**: Load GEMINI_API_KEY from env, implement SSE streaming with real Gemini API call
**Acceptance**: API endpoint streams back Gemini response using Server-Sent Events

### Step 12: Connect Frontend Button to Backend
**What**: Wire Promptify button to POST request, handle SSE stream, append chunks to output
**Acceptance**: Clicking button sends request, streams response into output textarea in real-time

### Step 13: Add Loading States
**What**: Button shows spinner + "Prompt engineer is working..." text while streaming
**Acceptance**: Button disabled during stream, shows loading UI, reverts when done

### Step 14: Implement Error Handling
**What**: Display error banner below panels for validation/API failures, preserve partial output
**Acceptance**: Invalid input or API error shows red error banner with message

### Step 15: Add Routing (/promptify base path)
**What**: Mount app at `/promptify`, redirect `/` to `/promptify`, adjust API path detection
**Acceptance**: Navigate to `/` redirects to `/promptify`, all routes work correctly

### Step 16: Style Polish and Responsive Refinement
**What**: Apply gradient backgrounds, transitions, focus states, shadows per spec
**Acceptance**: Visual appearance matches spec (gradients, borders, hover states, animations)

### Step 17: Add Microphone Button UI
**What**: Mic toggle button in input panel header with idle/active states and tooltip
**Acceptance**: Button displays, changes appearance when clicked, tooltip shows correct text

### Step 18: Implement Voice Dictation
**What**: Wire Web Speech Recognition API to mic button, append transcripts to input textarea
**Acceptance**: Clicking mic starts dictation, spoken words appear in textarea, red pulsing when active

### Step 19: Accessibility Pass
**What**: Add ARIA labels, ensure keyboard navigation, confirm contrast ratios, aria-live regions
**Acceptance**: Tab navigation works, screen reader announces states, WCAG contrast passes

---

## Remaining Elephant Parts (To Slice Later)

- **Advanced error recovery**: Retry logic, connection timeout handling, graceful degradation
- **Cross-browser compatibility**: Safari Speech API testing, Firefox fallback messaging
- **Performance optimization**: Debouncing, stream buffering, large input handling
- **Enhanced UX**: Keyboard shortcuts (Cmd+Enter to promptify), prompt history session storage
- **Production deployment**: Environment configuration, Docker setup, hosting instructions
- **Monitoring & logging**: Request tracking, error reporting, usage analytics
- **Extended accessibility**: High contrast mode, screen reader optimization, keyboard-only flow
- **Security hardening**: Rate limiting, input sanitization, CSP headers
- **Documentation**: User guide, API documentation, deployment guide

