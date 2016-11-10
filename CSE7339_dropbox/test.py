from __future__ import print_function

import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
import argparse

import dropbox
from dropbox.files import FolderMetadata, FileMetadata

TOKEN = '6YsZq1iVXHgAAAAAAAAAQ3SXdHSYGKZ_2y7VQ4RUjceDmgmwbx-GryZKJw7_JrxL'

parser = argparse.ArgumentParser(prog="dropboxfs", description='Sync ~/Downloads to Dropbox')
parser.add_argument('folder', nargs='?', default='/shabi',
                    help="Folder name in your Dropbox")
parser.add_argument('rootdir', nargs='?', default='~/Downloads',
                    help='Local directory to upload')
parser.add_argument('--token', default=TOKEN,
                    help='Access token '
                         '(see https://www.dropbox.com/developers/apps)')

parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')

dbx = dropbox.Dropbox("6YsZq1iVXHgAAAAAAAAAQ3SXdHSYGKZ_2y7VQ4RUjceDmgmwbx-GryZKJw7_JrxL")
dbx.users_get_current_account()

def main():
    """Main program.

    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """

    args = parser.parse_args()


    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        print('At most one of --yes, --no, --default is allowed')
        sys.exit(2)
    if not args.token:
        print('--token is mandatory')
        sys.exit(2)

    folder = args.folder
    rootdir = os.path.expanduser(args.rootdir)
    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a foldder on your filesystem')
        sys.exit(1)

    # strat scripting my own part

    # query files of the designated path
    #listing_downloads = list_folder(dbx, folder)

    #download_files_folders(folder, rootdir)
    res = list_folder(dbx, folder)
    print(res)
    #download files
    #download_files_folders(folder, rootdir)
    #upload files
    upload_files_folders(folder, rootdir)



def download_files_folders(dropbox_folder, local_folder):
    result = check_folder(dropbox_folder)
    #print(result)
    if result:
        # the path of a folder has been given
        listing_downloads = list_folder(dbx, dropbox_folder)
        for file in listing_downloads.entries:
            if not check_folder('/'.join([dropbox_folder, file.name])):
                print(dropbox_folder)
                path = str(dropbox_folder)
                filename = str(file.name)
                print(filename)
                download_path = os.path.join(local_folder, filename)
                dropbox_path = path + '/' + filename
                print(download_path)
                dbx.files_download_to_file(download_path, dropbox_path)
            else:
                next_local_dir = os.path.join(local_folder, file.name)
                next_remote_dir = '/'.join([dropbox_folder, file.name])
                if not os.path.exists(next_local_dir):
                    os.mkdir(next_local_dir)
                download_files_folders(next_remote_dir, next_local_dir)

    else:
        # the path of a file has been given to be downloaded
        dbx.files_download_to_file(local_folder, dropbox_folder)




def upload_files_folders(dropbox_folder, local_folder):
    result = os.path.isdir(local_folder)
    # print(result)
    if result:
        # the path of a folder has been given
        listing_uploads= os.listdir(local_folder)
        print("lsit of uploads files",listing_uploads)
        for file in listing_uploads:
            # do not upload those temparory files
            if file.startswith('.'):
                print('Skipping dot file:', file)
            elif file.startswith('@') or file.endswith('~'):
                print('Skipping temporary file:', file)
            elif not os.path.isdir('/'.join([local_folder, file])):
                print("local folder ==" ,local_folder)
                path = str(local_folder)
                filename = str(file)
                print(filename)

                upload_path = os.path.join(local_folder, filename)
                dropbox_path = dropbox_folder+ path + '/' + filename
                print(upload_path)
                dbx.files_upload(upload_path, dropbox_path)
            else:
                next_local_dir = os.path.join(local_folder, filename)
                next_remote_dir = '/'.join([dropbox_folder, filename])
                print("next_remote_dir",next_remote_dir)
                if not check_folder(next_remote_dir):
                    dbx.files_upload(next_local_dir, next_remote_dir)
                    # the path of a file has been given.
                    # upload the file
                    print("next_remote_dir",next_remote_dir)
                    # dbx.files_properties_update(next_remote_dir)
                else:
                    upload_files_folders(next_remote_dir, next_local_dir)

    else:
        # the path of a file has been given to be uploaded
        dbx.files_upload(local_folder, dropbox_folder)


# check is path given is a file or a folder.
def check_folder(checkfolder):

    try:
        folder_metedata = dbx.files_get_metadata(checkfolder)
    except Exception as e:
        print(e)
        return False
    is_folder = isinstance(folder_metedata, FolderMetadata)
    if is_folder:
        return True
    else:
        return False


def list_folder(dbx, folder):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s' % (folder)
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    res = dbx.files_list_folder(path)
    #for entry in res.entries:
        #print(entry.name)
    return res


if __name__ == '__main__':
    main()
