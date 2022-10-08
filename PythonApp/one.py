# MySQL queries

import pymysql

# Global variable
conn = None

# Connecting to database
def connection():
        global conn
        conn = pymysql.connect(host='localhost', user='root', cursorclass=pymysql.cursors.DictCursor, password='', db='moviesDB')



# Choice 1 - View films
# Query to get the filmname and actors who started in the films in alphabetical order
def view_films(choice):
          
        connection()
        
        sql = ('''select film.FilmName "Film", actor.ActorName "Staring" 
                from film, filmcast, actor 
                 where film.FilmID = filmcast.CastFilmID and actor.ActorID = filmcast.CastActorID
                order by Film, Staring''')

       
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
        
               


# Choice 2 - View actors by Year of birth and gender
# Query to get the year and gender of actors based on user input
def birth_gender(year, gender):
   
        connection()

        sql = ('''select ActorName, year(ActorDOB) as month, ActorGender from actor WHERE year(ActorDOB) LIKE %s and ActorGender LIKE %s ''') 
  
        cursor = conn.cursor()
        cursor.execute(sql, (year, gender))
        rows = cursor.fetchall()
        for row in rows:
                print(row['ActorName'], ':', row['month'], ':', row['ActorGender']) 
    


# Choice 2 - View actors by Year of birth and gender
# Query to get all actors born in the year inputting if no gender is specified
def birth(year):
  
        connection()

        sql = ('''select ActorName, year(ActorDOB) as month, ActorGender from actor WHERE year(ActorDOB) LIKE %s ''') 

        with conn:
                cursor = conn.cursor()
                cursor.execute(sql, (year))
                rows = cursor.fetchall()
                for row in rows:
                   print(row['ActorName'], ':', row['month'], ':', row['ActorGender'])



# Choice 3 - View studios
# Query to get all film studios 
def view_studio():
    
    connection()
 
    sql = ('''select * from studio order by StudioID''')

    with conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                x = cursor.fetchall()
                studios = x   # Assigned to variable so the database is only called once
                return studios
       



# Choice 4 - Add new coutry
# Query to add add a new country based on user input
def add_country(country_id, name):

      connection()
       
      sql = ('''INSERT INTO country (CountryID, CountryName) VALUES (%s, %s)''')

      with conn:
                try:
                        cursor = conn.cursor()
                        cursor.execute(sql, (country_id, name))
                        conn.commit()
                except pymysql.err.IntegrityError as e:
                        print('ERROR: ID/Country ({}/{}) already exists'.format(country_id, name)) # Error ID already exists
                except pymysql.err.DataError as e:
                        print('ERROR: ID/Country ({}/{}) already exists'.format(country_id, name)) # Error country already exists
                except Exception as e:
                        print(e)
                        
      


# Choice 5 - View film with subtitles
# Query to get the filmname and short synopsis for the filmid returned from the mongoDB query based off user input
def subtitles(filmid):
       
        connection()

        sql = ('''SELECT FilmId, FilmName, substring(FilmSynopsis, 1,30) as 'FilmSynopsis' FROM film WHERE filmid like %s''') 

        with conn:
                cursor = conn.cursor()
                cursor.execute(sql, (filmid))
                rows = cursor.fetchall()
                print(rows[0]['FilmName'], ':', rows[0]['FilmSynopsis'])
 



# Choice 6 - Add new movie script
# Query to see if the filmid exists in the database
def film_id(filmid):
      
        connection()

        sql = ('''SELECT filmid COUNT FROM film where filmid = %s''')

        with conn:
               
                cursor = conn.cursor()
                cursor.execute(sql, ('filmid'))
                row = cursor.fetchone()
                return row
      



# Choice 7 - View Films Oscar Wins and Nominations
# Query to view how many Oscars a film won
def oscar_wins():
           
               
        connection()
        sql =  ('select substring(FilmName, 1, 35) as "Film", FilmOscarWins as "OscarWins", FilmOscarNominations  as "Nominations" from film ORDER BY filmname')

        with conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                return rows




# Choice 8 - Certification and genre
# Query to view films by certification show their genre and synopsis
def certification(cert):
                
                connection()

                sql =  ('''SELECT g.genrename, f.filmname, f.filmsynopsis from film f INNER JOIN genre g ON f.filmgenreid = g.genreid INNER JOIN certificate c
                         ON f.filmcertificateid = c.certificateid WHERE c.certificate = %s ORDER BY filmname''')

                with conn:
                        cursor = conn.cursor()
                        cursor.execute(sql, (cert))
                        rows = cursor.fetchall()
                        for row in rows:
                                print(row['genrename'], '|', row['filmname'], '|', row['filmsynopsis'])
    


# Choice 9 - Box Office Hits by year     
# # Query to show films box office takings by year   
def top_grossing(year):
        
        connection()

        sql = ('''SELECT f.filmname, d.directorname, f.filmboxofficedollars as "Box Office $"  FROM film f INNER JOIN director d ON f.filmdirectorid = d. directorid
                WHERE year(f.filmreleasedate) = %s ORDER BY f.filmboxofficedollars DESC''') 

        with conn:
                cursor = conn.cursor()
                cursor.execute(sql, (year))
                rows = cursor.fetchall()
                for row in rows:
                        print(row['filmname'], '|', row['directorname'], '|', row['Box Office $'])




# Choice 10 - View actor by country 
# Query to show actors and their DOB based on country inputted by user
def actor(countryname):
        
        connection()

        sql = ('''SELECT a.actorname, date(a.actordob) as 'DOB' from  actor a INNER JOIN country c ON  a.actorcountryid = c.countryid WHERE c.countryname = %s ORDER BY a.actorname''') 

        with conn:
               cursor = conn.cursor()
               cursor.execute(sql, (countryname))
               rows = cursor.fetchall()
               for row in rows:
                        print(row['actorname'], '|', row['DOB'])
          