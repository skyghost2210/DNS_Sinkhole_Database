import mysql.connector
import DatabaseClient

class DatabaseConnect:

    def __init__ (self,hostName,databaseUser,userPassword,databaseName,authPlugin):
        self.host = hostName
        self.user = databaseUser
        self.passwd = userPassword
        self.database = databaseName
        self.authPlugin = authPlugin

    #Load data to database
    def load_to_database(self,insertDomains):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.database,
            auth_plugin = self.authPlugin
        )

        mycursor = mydb.cursor()

        numberOfInsertedDomains = 0
        numberOfDuplicatedDomains = 0

        for insertDomain in insertDomains:
            checkSQL="""SELECT EXISTS(SELECT * from domains WHERE domain LIKE (%s));"""
            val=(insertDomain, )
            mycursor.execute(checkSQL,val)
            result = mycursor.fetchone()[0]

            if result==0:
                sql = """INSERT INTO domains (domain) VALUES (%s)"""
                val = (insertDomain,)
                mycursor.execute(sql, val)
                numberOfInsertedDomains += 1
            else:
                numberOfDuplicatedDomains += 1

        mydb.commit()

        mycursor.close()
        mydb.close()

        return numberOfInsertedDomains,numberOfDuplicatedDomains