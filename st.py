import asyncio


async def main():
  await asyncio.sleep(1)
  print('hi')

asyncio.run(main())