import asyncio
from pathlib import Path
import aiofiles
import aiohttp
import argparse


async def main(n, folder, width, height):
    for i in range(n):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://picsum.photos/{width}/{height}?random={i}') as response:
                if response.status == 200:
                    f = await aiofiles.open(f'easy/{folder}/{i}.jpg', mode='wb')
                    await f.write(await response.read())
                    await f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image scraper for picsum.photos")
    parser.add_argument('-n', '--number', type=int, default=50,
                        help='How many images to download')
    parser.add_argument('-w', '--width', type=int, default=200,
                        help='Width of images')
    parser.add_argument('-v', '--height', type=int, default=300,
                        help='Height of images')
    parser.add_argument('-f', '--folder', dest="folder", action="store", type=str, default="images",
                        help='Folder for image storage')
    args = parser.parse_args()
    Path(f"easy/{args.folder}").mkdir(parents=True, exist_ok=True)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.number, args.folder, args.width, args.height))
