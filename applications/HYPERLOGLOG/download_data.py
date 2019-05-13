"""This script will check that we have all of our datasets available
    and download the ones that are not there.
"""
import os
import wget

to_download = [
"https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt",
"https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
]

names = [
"shakespeare.txt",
"english_words.txt"
]

for (resource, dest) in zip(to_download, names):
    if not os.path.exists(dest):
        print("Downloading %s..." % dest) 
        wget.download(resource, out = dest)

# set the contents to lowercase

for book in names:
    content = open(book).read().lower()
    open(book, "w").write(content)