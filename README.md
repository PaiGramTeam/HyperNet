# Hyper Network

Modern API wrapper for Endfield built on asyncio and pydantic.

## Requirements

- Python 3.9+
- httpx
- Pydantic

## Example

A very simple example of how HyperNet would be used:

```python3
import asyncio
import hypernet

async def main():
    cookies = {} # write your cookies
    player_id = 123456789
    async with hypernet.EndfieldClient(cookies, player_id=player_id) as client:
        data = await client.get_endfield_accounts()
        print(data)

asyncio.run(main())
```

## Credits

- [Skland_API](https://github.com/ProbiusOfficial/Skland_API)
- [arknights-toolbox](https://github.com/arkntools/arknights-toolbox)
- [arknights_bot](https://github.com/IJNKAWAKAZE/arknights_bot)
- [AUTO-MAS](https://github.com/AUTO-MAS-Project/AUTO-MAS)
