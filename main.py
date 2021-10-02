#!/usr/bin/python

''' 
- Pass in
    - directory to backup
    - site url
    - site backup location
    - username
    - password
    - port

- Zip up selected directory and place in /tmp
- FTP the zip to remote 
- Directory structure: <provided_location>/2021/Aug/filename.zip

'''

import argparse
from os import error
from backup import Backup
from ftp import FTP
from utils import eprint


def main():

    parser = argparse.ArgumentParser(description="FTP File Backup")

    # Local backup options
    parser.add_argument("-l", "--localdir", metavar="localdir", type=str, help="Local directory to backup", required=True)
    parser.add_argument("-o", "--outname", metavar="outname", type=str, help="Name of archive output", required=False)

    # Remote (FTP) options
    parser.add_argument("-H", "--host", metavar="host", type=str, help="Address of remote FTP host", required=True)
    parser.add_argument("-u", "--user", metavar="user", type=str, help="FTP user", required=True)
    parser.add_argument("-p", "--passwd", metavar="passwd", type=str, help="FTP password", required=True)
    parser.add_argument("-P", "--port", metavar="port", type=int, help="FTP port", default=21, required=False)
    parser.add_argument("-r", "--remotedir", metavar="remotedir", type=str, help="Remote backup directory", required=True)

    args = parser.parse_args()

    backup = Backup(args.localdir, args.outname)
    ftp = FTP(args.host, args.user, args.passwd, args.port)

    try:

        files = backup.run()

        ftp.connect()

        for file in files:
            ftp.sendfile(file, args.remotedir)

        backup.cleanup()

    except error as e:
        eprint("{0}".format(e))

    except FileNotFoundError:
        eprint("Specified directory does not exist")


if __name__ == "__main__":
    main()
