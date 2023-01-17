# async7zip
async7zip is an asynchronous interface for interacting with the 7-Zip command line tool. It allows for unpacking archive files in an asynchronous manner and provides properties for accessing the return code, error count, and process return code of the 7-Zip command.

Tested on 22.01 7-Zip english version.

### Installation
You can install async7zip via pip:

```
pip install async7zip
```

### Usage 
```python
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
```

### Note
Make sure to have `7zz` in your path, otherwise you need to specify path of `7zz` in `sevenzip_path`