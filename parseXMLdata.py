import os
import sys
import mysql.connector


#Connection to mysql DB
mydb0 = mysql.connector.connect(
    host = "localhost" ,
    user = "root" ,
    password = "" 
)

my_cursor = mydb0.cursor()

my_cursor.execute("CREATE DATABASE IF NOT EXISTS `internetandapplications`; ")

#connect to the created database
mydb = mysql.connector.connect(
    host = "localhost" ,
    user = "root" ,
    password = "" ,
    database = "internetandapplications"
)

my_cursor = mydb.cursor()

#if an error is raised
#it means that the tables
#already exist..
try:
    my_cursor.execute("CREATE TABLE `country` ( `nct_id` varchar(11) not NULL, `country_name` varchar(255) not NULL ); ")
    my_cursor.execute("CREATE TABLE `condition` ( `nct_id` varchar(11) not NULL, `cond` varchar(100) not NULL ); ")
    my_cursor.execute("ALTER TABLE `country` ADD KEY `nct_id` (`nct_id`); ")
    my_cursor.execute("ALTER TABLE `condition` ADD KEY `nct_id` (`nct_id`); ")    
    my_cursor.execute("COMMIT;")
except:
    pass



#grabs useful information from 
#the xml files.
def keep_useful_data ( filepath ):
    with open( filepath, "r", encoding="utf8" ) as fp:   #open file found
        countries = []
        condition = []
        nct_id = ""
        for line in fp :
            if "<nct_id>" in line:
                #keep the data inside the xml tags
                nct_id = line[line.find("<nct_id>")+len("<nct_id>"):line.rfind("</nct_id>")]
            elif ("    <country>" in line) and ("        " not in line):
                #keep the data inside the xml tags
                countries.append(line[line.find("    <country>")+len("    <country>"):line.rfind("</country>")])
            elif "<condition>" in line:
                #keep the data inside the xml tags
                condition.append(line[line.find("<condition>")+len("<condition>"):line.rfind("</condition>")])
    if(nct_id !=""):
        db_query( nct_id, countries,condition)


def db_query ( nct_id, countries,conditions):
    #remove "'" because we will have problems in the query
    nct_id = nct_id.replace("'","")
    
    #countries query
    if (len(countries) > 1) :
        for country in countries:
            country = country.replace("'","")
            query = "insert into `country` (nct_id , country_name) VALUES ('" + nct_id + "' , '" + country +"')"
            query.replace("''","NULL")
            query = query + ";"
            my_cursor.execute(query)
            mydb.commit()
    elif len(countries) == 1 :
        country = countries[0].replace("'","")
        query = "insert into `country` (nct_id , country_name) VALUES ('" + nct_id + "' , '" + country +"')"
        query.replace("''","NULL")
        query = query + ";"
        my_cursor.execute(query)
        mydb.commit()
    
    #conditions query
    if (len(conditions) > 1) :
        for condition in conditions:
            condition = condition.replace("'","")
            query = "insert into `condition` (nct_id , cond) VALUES ('" + nct_id + "' , '" + condition +"')"
            print(query)
            query.replace("''","NULL")
            query = query + ";"
            my_cursor.execute(query)
            mydb.commit()
    elif len(conditions) == 1 :
        condition = conditions[0].replace("'","")
        query = "insert into `condition` (nct_id , cond) VALUES ('" + nct_id + "' , '" + condition +"')"
        query.replace("''","NULL")
        query = query + ";"
        my_cursor.execute(query)
        mydb.commit()



#**************************MAIN*************************

#The second argument has to be the path
#to a directory that contains the xml 
#data( in the same directory or in subdirectories)

if (len(sys.argv)== 2):
    thisdir = sys.argv[1]
    # finds all files that end with xml 
    # in this directory or in any 
    # sub directory
    for r, d, f in os.walk(thisdir):    # r=root, d=directories, f = files
        for file in f:
            if file.endswith(".xml"):
                keep_useful_data(os.path.join(r, file))
    my_cursor.execute("SET SESSION old_alter_table=1;")
    my_cursor.execute("ALTER IGNORE TABLE `country` ADD UNIQUE INDEX u(nct_id);")
    my_cursor.execute("SET SESSION old_alter_table=0;")
else :
    print("Usage like: python parseXMLdata.py /path/to/xml/data")
