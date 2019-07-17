import asyncio
import aiohttp


class Crawler:
    def __init__(self, queue: asyncio.Queue):
        self.url = ''
        self.queue = queue

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str:
        async with session.get(url) as response:
            return await response.text()

    async def run(self) -> None:
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, self.url)
            await self.queue.put(item=response)

    def print_all(self) -> None:
        try:
            while True:
                print(self.queue.get_nowait())
        except asyncio.queues.QueueEmpty:
            pass

    async def gather(self):
        tasks = [
            asyncio.create_task(self.run())
            for _ in range(5)
        ]
        await asyncio.gather(*tasks)

    def main(self):
        asyncio.run(main=self.gather())
        self.print_all()


if __name__ == '__main__':
    queue = asyncio.Queue()
    crawler = Crawler(queue=queue)
    crawler.main()
