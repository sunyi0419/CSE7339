
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

'''
file_list = drive.ListFile({'q': "'0B60gqvrSzIJ4M3JEcGpmQV9hOVU' in parents"}).GetList()
for file1 in file_list:
  print('title: %s, id: %s' % (file1['title'], file1['id']))
exit()

'''




option = input("Upload , Download or query?")
if option.lower() == "upload":
  dir= input('Upload file directory.')
  file2 = drive.CreateFile()
  file2.SetContentFile(dir)
  file2['title'] = 'shen.txt'
  file2.Upload()
  print("You file:" + dir + " " + option.lower() + " completes")

elif option.lower() == "download":
  print("Downloading file")
  dir = input('Download file directory.')
  dir_div = dir.split("/") #split directory
  print (dir_div[0])
  #print(dir_div[1])
  print(len(dir_div))
  #exit()
  '''
  need to get the downloading file id first.
  list all the files and find its id.
  '''
#can only achieve download file.
#can add download folder by downloading each file in the folder one at a time, but before download make a directory in the local, folder.
  i = 0
  file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
  for file_srch in file_list:
    if file_srch['title'] == dir_div[i]:
      file3 = drive.CreateFile({'id': file_srch['id']})
      print(file_srch['title'])
      print(file_srch['id'])
      print('Downloading file %s from Google Drive' % file_srch['title'])
      file_srch.GetContentFile('shabi')


elif option.lower() == "query":
  dir = input('Query directory.')
  file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
  for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))

