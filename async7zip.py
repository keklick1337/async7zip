from asyncio.subprocess import Process
import asyncio
import enum

# Enum containing possible return codes of the unpack method
class ReturnCodes7zip(enum.Enum):
    SUCCESS = 0
    SUCCESS_WITH_SUBITEMS_ERRORS = 1
    ARCHIVES_WITH_ERRORS = 2
    WRONG_PASSWORD = 3
    UNEXPECTED_END_OF_ARCHIVE = 4
    OPEN_ERROR = 5
    NO_SUCH_FILE_OR_DIRECTORY = 6

class async7zip:
    """
    An async interface for interacting with the 7-Zip command line tool.
    Allows for unpacking archive files in an asynchronous manner.
    Provides properties for accessing the return code, error count, and process return code of the 7-Zip command.
    """
    def __init__(self, archive_path : str, unpack_path : str, password : str = "", sevenzip_path : str = "7zz") -> None:
        """
        Initializes the properties of the async7zip instance.
        
        :param archive_path: str - the path of the archive file to unpack
        :param unpack_path: str - the path to where the archive will be unpacked
        :param password: str - the password to use when unpacking the archive (default is empty string)
        :param sevenzip_path: str - the path to the 7-Zip command line tool (default is "7zz")
        """
        self.password = password
        self.archive_path = archive_path
        self.unpack_path = unpack_path
        self.sevenzip = sevenzip_path
        self.returncode : ReturnCodes7zip | None = None
        self.errors_subitems = 0
        self.errors_archive = 0
        self.errors_open = 0   
        self.process_returncode : int | None = None
        self.process : Process | None = None

    async def read_stdout(self):
        """
        Asynchronously reads the stdout of the 7-Zip process, and sets the returncode,
        errors_subitems, errors_archive, and errors_open properties based on the output.
        """
        while True:
            line = await self.process.stdout.readline()
            if not line:
                break
            decoded_line = line.decode(errors='replace').strip()
            if decoded_line == 'Everything is Ok':
                self.returncode = ReturnCodes7zip.SUCCESS
            elif decoded_line == 'Unexpected end of archive':
                self.returncode = ReturnCodes7zip.UNEXPECTED_END_OF_ARCHIVE
            elif decoded_line.startswith('Sub items Errors:'):
                try: self.errors_subitems = int(decoded_line.split(':')[-1].strip())
                except: pass
            elif decoded_line.startswith('Archives with Errors:'):
                try: self.errors_archive = int(decoded_line.split(':')[-1].strip())
                except: pass
                if self.returncode is None and self.errors_archive > 0:
                    self.returncode = ReturnCodes7zip.ARCHIVES_WITH_ERRORS
            elif decoded_line.startswith('Open Errors:'):
                self.errors_open = int(decoded_line.split(':')[-1].strip())
                if self.returncode is None and self.errors_open > 0:
                    self.returncode = ReturnCodes7zip.OPEN_ERROR
            elif decoded_line.startswith('ERROR: Wrong password'):
                self.process.kill()
                if self.returncode is None:
                    self.returncode = ReturnCodes7zip.WRONG_PASSWORD
                break
            elif decoded_line == 'ERROR: errno=2 : No such file or directory':
                self.process.kill()
                self.returncode = ReturnCodes7zip.NO_SUCH_FILE_OR_DIRECTORY

    async def unpack(self) -> ReturnCodes7zip | None:
        """
        Asynchronously unpacks the archive using the 7-Zip command and the properties
        set in the __init__ method. Returns the returncode property.
        """
        commandargs = ['x', '-y', '-bb', '-p{}'.format(self.password), self.archive_path, '-o{}'.format(self.unpack_path)]
        self.process = await asyncio.create_subprocess_exec(self.sevenzip, *commandargs, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        await asyncio.create_task(self.read_stdout())
        self.process_returncode = await self.process.wait()
        return self.returncode