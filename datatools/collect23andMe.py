#!/usr/bin/env python

import arvados
import arvados.collection
import sys
from arvados.arvfile import ArvadosFile
import os
import sqlite3
import re
import pandas as pd
import numpy as np

def main():

   # Create/find destination database
   newname23 = "PGP_23andMe_collection"
   ownerUUID = "su92l-j7d0g-nsjiqjm7jne7zgr"
   dest23 = findCollection(newname23,ownerUUID)

   # Load in huid, type and name from untap database
   conn = sqlite3.connect('db/hu-pgp.sqlite3')
   c = conn.cursor()
   c.execute('SELECT * FROM uploaded_data')
   rows = c.fetchall()
   dataPart = pd.DataFrame(rows,columns=zip(*c.description)[0])

   huid = dataPart.human_id.values
   huid = huid.tolist()
   url = dataPart.download_url.values
   datatype = dataPart.data_type
   datatype = datatype.tolist()

#   idx23 = dataPart.data_type == '23andMe'
#   url = dataPart[idx23].download_url.values
#   huid = dataPart[idx23].human_id.values
   
   n_url = url.shape[0]  

   urlnums = []

   for i in xrange(0,url.shape[0]):
     urlsplt = url[i].split("/")[-1]    
     urlnums.append(urlsplt)

   print(len(urlnums))   
   print(len(huid)) 
 
   # Create dictionaries
   source_dict = dict(zip(urlnums,huid))
   type_dict = dict(zip(urlnums,datatype))

   # Find number of elements in dictionaries
   print(len(source_dict))
   print(len(type_dict))

   # Project containing participant uploaded data
   project_uuid = "su92l-j7d0g-1d2se4f08r0q7ta"

   # Find collections
   c = arvados.util.list_all(arvados.api().collections().list,filters=[["owner_uuid","=", project_uuid]])
   n = len(c)
   
   cnumscc = []

   for nums1 in xrange(0,n):
     citer = c[nums1]
     cname = citer['name']
     ccnum = cname.split("--")[-1]
#     print(ccnum)
#     try:
     cc = arvados.collection.Collection(citer['uuid'])
     if ccnum in source_dict:
        chuid = source_dict[ccnum]
        ctype = type_dict[ccnum]
        if ctype == '23andMe':
          cnumscc.append(ccnum)
          for items in cc:
             target = "./"+chuid+"_"+items
             if not dest23.exists(target):
#               print("does not exist, copy "+ target)
               dest23.copy("./"+items,target_path=target,source_collection=cc,overwrite=True)
          dest23.save()
#        else:
#           print("Can not find huid for " + cname)
#     except:
#        print("Can't access " + cname) 
 
   print(len(cnumscc))


def findCollection(newname,owner):
   
   newcol = arvados.api().collections().list(filters=[["name","=",newname]]).execute()

   # If collection doesn't exist, make it
   if newcol['items_available']==0:
      dest = arvados.collection.Collection()
      dest.save_new(name=newname,owner_uuid=owner)
   else:
      newcol = newcol.items()[1][1][0]
      dest = arvados.collection.Collection(newcol['uuid'])
   return dest


if __name__ == '__main__':
  main()

