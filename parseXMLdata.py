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
    my_cursor.execute("CREATE TABLE `trials` ( `nct_id` varchar(11) not NULL, `official_title` varchar(360) DEFAULT NULL,`brief_title` varchar(360) DEFAULT NULL, `acronym` varchar(255) DEFAULT NULL ); ")
    my_cursor.execute("CREATE TABLE `condition` ( `nct_id` varchar(11) not NULL, `cond` varchar(100) not NULL ); ")
    my_cursor.execute("CREATE TABLE `mesh_term` ( `nct_id` varchar(11) not NULL, `term` varchar(100) not NULL); ")
    my_cursor.execute("ALTER TABLE `country` ADD KEY `nct_id` (`nct_id`); ")
    my_cursor.execute("ALTER TABLE `trials` ADD KEY `nct_id` (`nct_id`); ")
    my_cursor.execute("ALTER TABLE `condition` ADD KEY `nct_id` (`nct_id`); ")
    my_cursor.execute("ALTER TABLE `mesh_term` ADD KEY `nct_id` (`nct_id`); ")
    my_cursor.execute("ALTER TABLE `country` ADD CONSTRAINT `country_ibfk_1` FOREIGN KEY (`nct_id`) REFERENCES `trials` (`nct_id`); ")
    my_cursor.execute("ALTER TABLE `condition` ADD CONSTRAINT `condition_ibfk_1` FOREIGN KEY (`nct_id`) REFERENCES `trials` (`nct_id`); ")
    my_cursor.execute("ALTER TABLE `mesh_term` ADD CONSTRAINT `mesh_term_ibfk_1` FOREIGN KEY (`nct_id`) REFERENCES `trials` (`nct_id`); ")
    my_cursor.execute("COMMIT;")
except:
    pass



#grabs useful information from 
#the xml files.
def keep_useful_data ( filepath ):
    with open( filepath, "r", encoding="utf8" ) as fp:   #open file found
        countries = []
        mesh_terms = []
        condition = []
        off_title = ""
        brief_title = ""
        acronym = ""
        nct_id = ""
        for line in fp :
            if "<official_title>" in line:
                #keep the data inside the xml tags
                off_title = line[line.find("<official_title>")+len("<official_title>"):line.rfind("</official_title>")]
            elif "<brief_title>" in line:
                #keep the data inside the xml tags
                brief_title = line[line.find("<brief_title>")+len("<brief_title>"):line.rfind("</brief_title>")]
            elif "<acronym>" in line:
                #keep the data inside the xml tags
                acronym = line[line.find("<acronym>")+len("<acronym>"):line.rfind("</acronym>")]
            elif "<nct_id>" in line:
                #keep the data inside the xml tags
                nct_id = line[line.find("<nct_id>")+len("<nct_id>"):line.rfind("</nct_id>")]
            elif "    <country>" in line:
                #keep the data inside the xml tags
                countries.append(line[line.find("    <country>")+len("    <country>"):line.rfind("</country>")])
            elif "    <country>" in line:
                #keep the data inside the xml tags
                countries.append(line[line.find("    <country>")+len("    <country>"):line.rfind("</country>")])
            elif "<condition>" in line:
                #keep the data inside the xml tags
                condition.append(line[line.find("<condition>")+len("<condition>"):line.rfind("</condition>")])
            elif "<mesh_term>" in line:
                #keep the data inside the xml tags
                mesh_terms.append(line[line.find("<mesh_term>")+len("<mesh_term>"):line.rfind("</mesh_term>")])
    if(nct_id !=""):
        db_query( off_title, brief_title, acronym, nct_id, countries,condition,mesh_terms)


def db_query ( off_title, brief_title,  acronym, nct_id, countries,conditions,mesh_terms):
    #remove "'" because we will have problems in the query
    nct_id = nct_id.replace("'","")
    off_title = off_title.replace("'","")
    brief_title = brief_title.replace("'","")
    acronym = acronym.replace("'","")
    
    #make the query 
    query = "insert into `trials` (nct_id , official_title, brief_title, acronym) VALUES ('" + nct_id + "' , '" + off_title + "' , '" + brief_title + "' , '" + acronym+ "')"
    query.replace("''","NULL")
    query = query + ";"
    
    #execute query
    my_cursor.execute(query)
    mydb.commit()
    
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
        print(query)
        query.replace("''","NULL")
        query = query + ";"
        my_cursor.execute(query)
        mydb.commit()

    #mesh_terms query
    if (len(mesh_terms) > 1) :
        for mesh_term in mesh_terms:
            mesh_term = mesh_term.replace("'","")
            query = "insert into `mesh_term` (nct_id , term) VALUES ('" + nct_id + "' , '" + mesh_term +"')"
            query.replace("''","NULL")
            query = query + ";"
            my_cursor.execute(query)
            mydb.commit()
    elif len(mesh_terms) == 1 :
        mesh_term = mesh_terms[0].replace("'","")
        query = "insert into `mesh_term` (nct_id , term) VALUES ('" + nct_id + "' , '" + mesh_term +"')"
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
else :
    print("Usage like: python parseXMLdata.py /path/to/xml/data")
