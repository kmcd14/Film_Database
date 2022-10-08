# Applied Databases 2021 Project
# G00398279 - Katie Mc Donald 


# Importing Modules/Libraries
import pymysql 
import pymongo
import one # MySQL queries
import two # Mongodb queries
import pandas as pd 


# Title menu
def title_menu():
        print('\t\t\tMENU\n*******************************************************************************')
        print('\t1 - View Films')
        print('\t2 - View Actors By Year Of Birth & Gender')
        print('\t3 - View Studios')
        print('\t4 - Add New Country')
        print('\t5 - View Movie With Subtitles')
        print('\t6 - Add New Movie Script')
        print('\t7 - View Films Oscar Wins and Nominations')
        print('\t8 - Certification and Genre')
        print('\t9 - Box Office Hits by Year')
        print('\t10 - View Actors by Country')
        print('\tx- Exit Application')    
        print('*******************************************************************************************')
        


# Main Programme
def main():
    title_menu()

    # Main Loop
    while True:
        choice = input('\nPlease choose a number to continue: ').lower() # Getting user input
       
        # View Films
        if choice == "1":
            print('**************************************************************************')
            print('\t\t\tFILMS\n**************************************************************************')
            
            while True:    
                 rows = one.view_films(choice)
                 movies_df = pd.DataFrame(rows)  # Creating a dataframe 
                 start_row = 0
                 ending_row = start_row + 5 # Showing in groups of 5

                # Loop through input
                 while True:
                     
                     should_continue = input('--------------------------------------\n****Press q to quit, otherwise press any key: *****').lower()
                     if should_continue == 'q':
                         
                         title_menu() # If 'q' is entered return to the title menu
                         break
                        
                     else:
                    # Subset to the next 5 movies
                        set_of_5 = movies_df.loc[start_row: ending_row]
                    #should_continue = input('')

                    # Print headers
                     print('******************************')
                     print('Movie Name  ||   Staring')
                     print('******************************')
                     for idx, row in set_of_5.iterrows():
                        print(f'{row.Film} ||  {row.Staring}') # Formatting
                    
                    # Prompt user for input
                    
                    # Check to continue
                     if should_continue != 'q':
                        # If the user didn't type 'q', get the next 5 rows
                        start_row = ending_row + 1
                        ending_row = ending_row + 5

                     else:
                        # Otherwise, break the loop
                        break
                 break 


       
        # View Actors By Year Of Birth & Gender
        elif  choice == '2':
            while True:
                try:
                    dob = int(input('Enter year of birth: ')) # Getting the date
                except ValueError:
                    print('Please enter a vaild year: ') # If input is not an integer repeat
                    continue
                while True: 
                        gender = input('Gender (Male/Female): ').lower()
                        if gender == 'male' or gender == 'female':
                            one.birth_gender(dob, gender)
                            break
                        elif gender == '':  # If no gender is entered show all actors born the year entered
                            one.birth(dob)
                            break
                        else:
                            print('Please enter a gender: ')              
                            continue
            
                title_menu() # Return to title menu
                break
            


       
        # View Studios
        elif choice == '3':
            rows = one.view_studio() # MySQL query to get all studios
            studios = rows 
            for row in studios:
                print(row['StudioID'], ':', row['StudioName'])
       


       
        # Add new country
        elif choice == '4':
            print('Add New Country')
            print('*******************')
            while True:
                try:
                    country_id = int(input('enter id: ')) 
                    print(country_id)  
                except ValueError:
                    print('Invaild input') # If input isn't an integer repeat
                    continue
                while True:
                    name = input('Enter name: ').lower()
                    if name == '': 
                        try:
                            continue # Repromt for a name if left blank
                        except:
                            break                    
                    else:
                        break   
                one.add_country(country_id, name) # Call SQL query
                break




        # View movies with subtitles
        elif choice == '5':
            print('Movies With Subtitles')
            print('*******************')
            while True:
                    sub_language = input('Enter subtitle language: \n------------------------------------------------------------')
                    if sub_language == '': 
                        continue
                    else:
                        break
            
            while True:
              results = two.find(sub_language) # Calling mongoDB query to find films containing the entered subtitle language
              for result in results:
                x = result['_id']
                one.subtitles(x) # Calling the MySQL query which returns the name and short synopsis of the film with the corresponding film id from the mongoDB query
                
              break 
          

              
        # Add new movie script
        elif choice == '6':
            print('Add New Movie Script')
            print('*******************')
            scripts = {} # Empty dict
            while True:
                try:
                    filmid = int(input('enter id: '))
                except ValueError:
                    print('Invaild input') # Prompt user again if id entered isn't an integer
                    continue
                while True:
                    keywords = input('Keyword <-1 to end>: ') 
                    if keywords != '-1': # Get keywords until user enters '-1'
                        continue
                    else: 
                        while True:
                            subtitles = input('Subtitles Language <-1 to end>: ')     
                            if subtitles != '-1': # Get subtitle language until user enters '-1'
                                continue
                            else:  
                                break 
                        break
                break        
            
            while True:
                x = one.film_id(filmid) # MySQL query to search database for a corresponding filmid
                if x == 0:
                            print('ERROR: ID does not exists') # If id can't be found 
                            break
                
                # Adding user input into the empty dict scripts
                scripts['_id'] = filmid  
                scripts['keywords'] = keywords
                scripts['subtitles'] = subtitles   
                two.new_script(scripts) # MongoDB query to add the new script
                break



        elif choice == '7':
            while True:    
                 rows = one.oscar_wins()
                 movies_df = pd.DataFrame(rows) # Creating a dataframe
                 start_row = 0
                 ending_row = start_row + 10 # Showing in groups of 10

                # Loop through input
                 while True:
                     
                     should_continue = input('-------------------------------------------------------------------------\n****Press q to quit, otherwise press any key: *****').lower()
                     if should_continue == 'q':
                         
                         title_menu() # If 'q' is entered return to the title menu
                         break
                        
                     else:
                    # Subset to the next 5 movies
                        set_of_10 = movies_df.loc[start_row: ending_row]
                    #should_continue = input('')

                    # Print headers
                     print('*************************************************************')
                     print('     Movie     ||         Oscar Wins   ||   Oscar Nominations')
                     print('*************************************************************')
                     for idx, row in set_of_10.iterrows():
                         print('{:25}|     {:2}     | {:10}'.format(row.Film, row.OscarWins, row.Nominations))
                       # print(f'{row.Film} |\t  {row.OscarWins} |\t {row.Nominations}') # Formatting
                    
                    # Prompt user for input
                    
                    # Check to continue
                     if should_continue != 'q':
                        # If the user didn't type 'q', get the next 10 rows
                        start_row = ending_row + 1
                        ending_row = ending_row + 10

                     else:
                        # Otherwise, break the loop
                        break
                 break 



        # Certification and Genre
        elif choice == '8':
            print('**************************Certification****************************')
            while True:
                cert =  input('Please choose a Certificate: U, PG, 12, 12A, 15 or 18: \n').upper() # Making imput uppercase so it works while checking the list
                if cert not in ['U', 'PG', '12', '12A', '15', '18']:
                        print('Please choose a Certificate: U, PG, 12, 12A, 15 or 18: \n')
                        continue
                else: 
                         one.certification(cert) # MySQL function to return films with the entered certificate and a synopsis
                         break
                break



        # Box Office Hits by Year
        elif choice == '9':
           
            while True:
                try:
                    year = int(input('Enter year: ')) # Getting year
                    break
                except ValueError:
                    # print('Enter year: ') # If input is not an integer repeat
                    continue
            print('***** Film    |  Director  | Box Office Takings ($) ******')
            print('=================================================================')
            one.top_grossing(year)



        
        # View Actor and thie DOB by country
        elif choice == '10':
            while True:
                countryname = input("-------------------------------------------------------\nPlease Enter a Country or 'q' to quit: ").lower() # Getting country from user
                if countryname == 'q': # Quit if user enters 'q'
                    break
                else:
                    print('Actor      |     DOB')
                    print('*****************************************************')
                    one.actor(countryname)
            
            title_menu()



        # Exit programme if user inputs 'x'
        elif choice == 'x':
            exit()    




        # If the user inputs anything the title menu options, keep displaying the title menu    
        else:
            title_menu()
                   
  



if __name__ == "__main__":
       main()
