import os

from tempfile import gettempdir
from shutil import make_archive
from datetime import datetime
from utils import eprint


class Backup:

    def __init__(self, dir, outname=None) -> None:
        self._dir = dir
        self._outname = self._get_outname(outname)
        self._sys_temp = self._get_sys_temp()
        self._files_created = []

    def _get_sys_temp(self) -> str:
        return gettempdir()

    def _get_outname(self, outname) -> str:
        if not outname:
            now = datetime.now()
            return now.strftime("%d_%b_%Y_%H%M%S")
        return outname.replace(" ", "_").lower()

    def _zip_dir(self) -> None:
        os.chdir(self._sys_temp)
        self._files_created.append(make_archive(self._outname, "zip", self._dir))

    # Executes the backup returning a list of backup locations
    def run(self) -> list:
        self._zip_dir()
        return self._files_created

    # Delete all temp files created by the backup
    def cleanup(self) -> None:

        if len(self._files_created) == 0:
            return

        for file in self._files_created:
            try:
                os.remove(file)
            except os.error:
                eprint("Failed to cleanup %s" % file)
