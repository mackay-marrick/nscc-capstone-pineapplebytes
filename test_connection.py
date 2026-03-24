import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Unlock the .env file to get the API key
load_dotenv()

# 2. Set up the client to point to OpenRouter instead of OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 3. Send a simple ping to the free model you selected
try:
    print("Sending ping to OpenRouter...")
    response = client.chat.completions.create(
        model="stepfun/step-3.5-flash:free",
        messages=[{"role": "user", "content": "Reply with only the words: 'Connection Successful!'"}]
    )
    # 4. Print the AI's response
    print("\nResponse received:")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\nConnection failed! Error details:\n{e}")  