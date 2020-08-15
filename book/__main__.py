import asyncio
import logging
from aiohttp import web
from book.webserver import web_server


async def main():
    runner = web.AppRunner(await web_server())
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", 8080).start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        logging.info("Site Started")
        loop.run_forever()
    except KeyboardInterrupt as e:
        logging.error(f"Site Interrupted with KeyboardInterrupt")
        loop.stop()
    finally:
        logging.info("Site Terminated")
