# drc_test

To run this code in a virtual env first go to the desired loation where you want to set up the project.
Open terminal there and run the command:
  python3 -m venv env # where env is the name of your virtual env
To activate our virtual env 
  **ForLinux users**
  > source env/bin/activate
  **For Windows Users**
  > ./env/Scripts/activate

Run the following command to install the dependencies
  > pip install -r requirements.txt

Configure the Database, I had added my conf file for help.
Afer that, run the following commands to host project
  > python manage.py makemigrations
  > python manage. migrate
  > python manage.py runserver

The first wo commands will update the database with all the required fields and there validations.
The last command will host the project on localhost:8000


**For creating user =>** localhost:8000/api/create/ (POST)
Parameters 
  > username
  > mobile
  > email
  > password
  > age(optional)
 *Username and email are kept unique*
 
 **For login =>** localhost:8000/api/login/ (POST)
 Parameters
  > mobile
  
 **For verification of otp =>** localhost:8000/api/verify/<otp> (GET)
  Parameters
    > otp
  
  **For updating users email through profile page => ** localhost:8000/api/update/ (PATCH)
  Parameters
    > email_id
    > user (user id)
  
 
