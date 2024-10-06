from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def handle_ai_question(ctx, question):
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are SGT Dickburgler, a helpful assistant for a military Discord server. The current date and time is {current_time}, and you are in El Paso, Texas (Mountain Time Zone)."},
                {"role": "user", "content": question}
            ]
        )
        await ctx.send(response.choices[0].message.content)
    except Exception as e:
        await ctx.send(f"An error occurred while processing your question: {str(e)}")

# Add more AI-related functions as needed