import asyncio
from dotenv import load_dotenv
import os
import sys
from aiogram import Bot,Dispatcher,types
from openai import AsyncOpenAI
from aiogram.filters import CommandStart

class Refrence():
    '''
    A class to refrence of previously conversation in open ai
    '''
    def __init__(self) -> None:
        self.response=""

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("API_KEY"))

refrence = Refrence()

MODEL_NAME = 'gpt-3.5-turbo'

TOKEN = os.getenv('TOKEN')
print(TOKEN)

dispatcher = Dispatcher()

def clear_past():
    '''A method to clear previous context and conversation'''
    refrence.response=""

@dispatcher.message(CommandStart())
async def welcome(message: types.message):
    '''This handler to receive message with /start or /help command'''
    await message.reply("Hi\nI am Telebot created by:Nishant\nHow can I Help you")

@dispatcher.message()
async def chatbot(message: types.message):
    '''This handler to proccessed message throgh openai'''
    print(f"User: {message.text}")

    response = await client.chat.completions.create(
        messages = [
            {"role":"assistant","content":refrence.response},
            {"role":"assistant","content":message.text}
        ],
        model=MODEL_NAME,
    )

    refrence.response = response['choices'][0]['message']['content']
    print(f"ChatGpt: {refrence.response}")
    message.reply(f"Chat Id={message.Chat.id} text={refrence.response}")


async def main()->None:
    bot = Bot(token=TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())