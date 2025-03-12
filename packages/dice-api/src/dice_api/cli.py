from __future__ import annotations

import asyncio

import uvicorn


async def serve() -> None:
    config = uvicorn.Config(
        "dice_api.app:app",
        host="0.0.0.0",
        port=4935,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


def main() -> None:
    asyncio.run(serve())


if __name__ == "__main__":
    main()
