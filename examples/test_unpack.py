import asyncio
from async7zip import async7zip, ReturnCodes7zip

async def main():
    # Initialize the async7zip object
    sevenzip = async7zip(archive_path='path/to/archive.7z', unpack_path='path/to/unpack')

    # Unpack the archive
    return_code = await sevenzip.unpack()

    # Check the return code
    if return_code == ReturnCodes7zip.SUCCESS:
        print("Archive unpacked successfully!")
    else:
        print(f"Error code: {return_code}")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())