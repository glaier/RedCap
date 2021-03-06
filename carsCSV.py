import os
import re
import zipfile
import html

#In SPSS, SAS and Stata use export functions to save data files as CSV files with variablenames
#without special characters and white spaces.

#Special characters in the csv file are converted to HTML codes readable to RedCap

#Input information

#Table/Instrument name
#Replace blanks with underscore
name_table="FLOW_database_NHL"

#Table with input data, variable names in first row
table_file_name="L:/LovbeskyttetMapper/DataGovernanceWP15/"+name_table+".csv"

#File with instrument header in RedCap format
first_line="Variable / Field Name,\"Form Name\",\"Section Header\",\"Field Type\",\"Field Label\",\"Choices, Calculations, OR Slider Labels\",\"Field Note\",\"Text Validation Type OR Show Slider Number\",\"Text Validation Min\",\"Text Validation Max\",Identifier?,\"Branching Logic (Show field only if...)\",\"Required Field?\",\"Custom Alignment\",\"Question Number (surveys only)\",\"Matrix Group Name\",\"Matrix Ranking?\",\"Field Annotation\"\n"
print(first_line)
second_line="record_id,"+name_table+",,text,\"Record ID\",,,,,,,,,,,,,,\n"
print(second_line)

#RedCap text variable instrument file format leaving value labels and notes out
text_var_format=",,text,,,,,,,,,,,,,,\n"

#Generated folder with instrument import zip file
path_instrument_zip_file = "L:/LovbeskyttetMapper/DataGovernanceWP15/RedCap_"+name_table

try:
    os.mkdir(path_instrument_zip_file)
except OSError:
    print ("Creation of the directory %s failed" % path_instrument_zip_file)
else:
    print ("Successfully created the directory %s " % path_instrument_zip_file)

os.chdir(path_instrument_zip_file)

#Output file with header rows
fout = open("instrument.csv", "wt")
fout.write(first_line)
fout.write(second_line)
fin = open(table_file_name,"rt")

variable_names=fin.readline().lower().replace("å","aa").replace("ø","oe").replace("æ","ae")
variable_names=variable_names.rstrip()
variable_names=variable_names.replace(",","_text,")
variable_list=variable_names.split(",")
print(variable_list)
fin.close()

for varname in variable_list:
    fout.write((varname+","+name_table+text_var_format).lower())
fout.close()
fout = open("OriginID.txt", "wt")
fout.write("redcap.regionh.dk\n")
fout.close()

# writing files to a zipfile
zip_file = zipfile.ZipFile("RedCap_"+name_table+".zip", "w")
zip_file.write("OriginID.txt")
zip_file.write("instrument.csv")
zip_file.close()

print("RedCap"+name_table+'.zip file is created successfully!')

#Add record_id temporary index variable to csv file
fin=open(table_file_name,"rt")
lines=fin.readlines()

fout=open(name_table+"_id.csv","wt")
fout.write("record_id,"+variable_names+"\n")

i=0
for line in lines:
    if i!=0:
        fout.write(str(i)+html.escape(line).encode('ascii', 'xmlcharrefreplace').decode())
    i=i+1

fin.close()
fout.close()