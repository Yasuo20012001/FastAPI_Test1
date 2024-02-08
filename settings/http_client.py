import asyncio
import aiohttp


class HttpClient:
    session: aiohttp.ClientSession = None

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        if self.session:
            await self.session.close()
        self.session = None

    async def fetch_with_retry(self, url, method="GET", retries=3, timeout=60000, headers=None, json_data=None):
        for i in range(retries):
            try:
                async with self.session.request(
                    method, url, timeout=timeout, headers=headers, json=json_data
                ) as response:
                    return await response.content.read()
            except:  # noqa E 401
                if i == retries - 1:
                    raise
                await asyncio.sleep(1)

    def __call__(self) -> aiohttp.ClientSession:
        assert self.session is not None
        return self.session


http_client = HttpClient()


def get_http_client() -> HttpClient:
    return http_client
