from app.core.gemini import ask_gemini


response = ask_gemini(
    "Reply with exactly: Gemini is working"
)

print(response)