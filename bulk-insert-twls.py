
import io, glob, os, csv, re

wordStrongsGrabber = r"\\w (\W*)\|.*?strong=\"(?:\w?:?){0,2}(H\d{4})"
twbaselink = "rc://*/tw/dict/bible"

with io.open("twlinksindex.txt", encoding='utf8') as f:
    twlinkslist = f.readlines()