import logging

import aiohttp


async def upload_check(transaction_id: int, check: bytes) -> str | None:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                'http://app:8000/save-image',
                data={
                    'secret': '228322aza',
                    'transaction_id': transaction_id,
                    'image_input': check,
                },
            ) as r:
                return (await r.json())['path']
    except Exception as e:
        logging.error(e.__class__.__name__)
        return None
