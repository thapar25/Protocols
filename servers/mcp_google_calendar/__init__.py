from .server import serve


def main():
    """MCP Google Calendar Server - Read user calendar functionality for MCP"""
    import asyncio
    asyncio.run(serve())


if __name__ == "__main__":
    main()