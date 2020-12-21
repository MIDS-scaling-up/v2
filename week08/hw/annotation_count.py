import xml.etree.ElementTree as ET
import os
from collections import Counter
def read_content(xml_file: str):
   tree = ET.parse(xml_file)
   root = tree.getroot()
   list_with_all_names = []
   for names in root.iter("object"):
       list_with_all_names.append(names.find("name").text)
   return list_with_all_names
listTally = []
directory =os.fsencode('annotations')
num_files = len([f for f in os.listdir(directory)if os.path.isfile(os.path.join(directory, f))])
for file in os.listdir(directory):
   filename = os.fsdecode(file)
   print(os.path.join(os.fsdecode(directory), filename))
   input = os.path.join(os.fsdecode(directory), filename)
   temp = read_content(input)
   listTally.append(temp)
print("num files", num_files)
flat_list = [item for sublist in listTally for item in sublist]
# print(flat_list)
print(Counter(flat_list))
