#!/usr/bin/env python

import arvados
import arvados.collection
import sys
from arvados.arvfile import ArvadosFile


def main():

   # Find (or create) collections to contain the sorted BAM and VCF files
   newnameVCF = "PGP_vcf_collection"
   destVCF = findCollection(newnameVCF)

   newnameBAM = "PGP_bam_collection"
   destBAM = findCollection(newnameBAM)

   # Project containing PGP data
   project_uuid = "su92l-j7d0g-d000kgavzol8a8g"

   # Find subprojects
   subprojs = arvados.util.list_all(arvados.api().groups().list,filters=[["owner_uuid","=", project_uuid],["group_class","=",'project']])
   n = len(subprojs)

   for nums1 in xrange(0,n):
      uuid = subprojs[nums1]['uuid']
      name = subprojs[nums1]['name']
      print(name)
      # Find subprojects
      subprojs2a = arvados.util.list_all(arvados.api().groups().list,filters=[["owner_uuid","=", uuid],["group_class","=","project"],["name","like","%datasets"]])
      for nums2 in xrange(0,len(subprojs2a)):
         uuid2 = subprojs2a[nums2]['uuid']
         name2 = subprojs2a[nums2]['name']
         # Find collections containing keyword and copy over files
         copyFiles(uuid2,'.vcf',destVCF,name)
         copyFiles(uuid2,'.bam',destBAM,name)

def findCollection(newname):
   newcol = arvados.api().collections().list(filters=[["name","=",newname]]).execute()

   # If collection doesn't exist, make it
   if newcol['items_available']==0:
      dest = arvados.collection.Collection()
      dest.save_new(name=newname)
   else:
      newcol = newcol.items()[1][1][0]
      dest = arvados.collection.Collection(newcol['uuid'])
   return dest

def copyFiles(uuid,keyword,dest,name):
    c = arvados.util.list_all(arvados.api().collections().list,filters=[["owner_uuid","=", uuid],["name","like","%"+keyword]])

    for nums3 in xrange(0,len(c)):
       citer = c[nums3]
       cc = arvados.collection.Collection(citer['uuid'])
       for items in cc:
         target = "./"+name+"_"+items
         if not dest.exists(target):
           print("does not exist, copy "+ target)
           dest.copy("./"+items,target_path=target,source_collection=cc,overwrite=True)
       dest.save()


if __name__ == '__main__':
  main()         
