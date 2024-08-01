import asyncio
import bot


async def main():
    bot.dp.message.outer_middleware(bot.Text())
    await bot.dp.start_polling(bot.bot)
    

if __name__ == '__main__':
    try:
       asyncio.run(main())
    except:
        print('Бот выключен')

