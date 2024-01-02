import openai

# Set your OpenAI API key here
api_key = "YOUR_API_KEY"

# Connect to the OpenAI API
openai.api_key = api_key

def chat_with_gpt(engine, prompt, max_tokens=100, n=1, stop=None, temperature=0.7):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature
    )
    return response.choices[0].text.strip()

def chat_with_gpt3(prompt, max_tokens=100, n=1, stop=None, temperature=0.7):
    return chat_with_gpt("text-davinci-003", prompt, max_tokens, n, stop, temperature)

def chat_with_gpt4(prompt, max_tokens=100, n=1, stop=None, temperature=0.7):
    return chat_with_gpt("text-davinci-004", prompt, max_tokens, n, stop, temperature)
