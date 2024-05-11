import aiohttp
import asyncio
import pydantic


class Response(pydantic.BaseModel):
    id: int


async def fetch_data(url) -> Response:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.json()
            return pydantic.TypeAdapter(Response).validate_python(resp)


async def main():
    resp = await fetch_data('https://dummyjson.com/products/1')
    print('Product ID', resp.id)


if __name__ == '__main__':
    asyncio.run(main())
