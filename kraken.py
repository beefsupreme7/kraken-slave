from io import BytesIO

import requests, os, zipfile, shutil

jobsURL = 'https://github.com/timeline.json'
downloadURL = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
uploadURL = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
id = 0
status = 'open'

def getJobs(url):
    j = requests.get(url)
    # status = blocked
    jobList = j.json()
    return jobList

# def getParameters(jobList):
#     global id = jobList['id']
#     global downloadURL = jobList['downloadURL']
#     global uploadURL = jobList['uploadURL']
#     global status = jobList['status']

# file downloaden
def getFile(url):
    if not os.path.exists('DATA/downloadedzip'):
        os.makedirs('DATA/downloadedzip')

    r = requests.get(url)
    dump = r
    location = os.path.abspath("DATA/downloadedzip/code2.zip")
    with open("code2.zip", 'wb') as location:
        shutil.copyfileobj(dump, location)

# zip Archiv entpacken
def unzip(srcpath, zipname, dstpath):
    if not os.path.exists(srcpath):
        os.makedirs(srcpath)
    zfile = zipfile.ZipFile(srcpath + zipname)
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)
        print('UNZIP: ' + filename + ' from ' + srcpath + zipname + ' to ' + dstpath)

        zfile.extract(name, dstpath)

# zip Archiv erstellen
def zip(srcpath, zipname, dstpath):
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    zfile = zipfile.ZipFile(dstpath + zipname, 'w', zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(srcpath)
    for dirname, subdirs, files in os.walk(srcpath):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('ZIP: ' + srcpath + filename + ' to ' + dstpath + zipname)
            zfile.write(absname, arcname)
    zfile.close()

getFile(downloadURL)

# Archiv entpacken aus /DATA/downloadedzip in /DATA/extractedzip
unzip('DATA/downloadedzip/', 'code2.zip', 'DATA/extractedzip/')
print('')

# Archiv erstellen aus /DATA/extractedzip in /DATA/resultzip
zip('DATA/extractedzip/', 'result.zip', 'DATA/resultzip/')
print('')

jobList = getJobs(jobsURL)
print(jobList['message'])
