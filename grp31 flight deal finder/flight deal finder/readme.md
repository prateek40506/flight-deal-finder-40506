#DBMS Lab Report

People often dream of going to places but don’t find a suitable platform that offers flight suggestions according to user budget, so this is what our website has in store for our beloved users:
##Brief Description
It will involve a front-end page which requires the user to enter his/her flight requirements like the destination, number of days of visit, number of seats you wish to book and the budget of travel. Based on the search, the user will receive a list of possible flights available. He/she can then select one of them and the status of the selection will be stored in the database. There will be a table for storing all the user search requests and another table for the available flight details and it will be referenced to the first table so that the search results are mapped to the search queries.
##Basic Flow of the site
First the user logins to our site. He/She requires to fill a google sheet where in he/she needs to fill up the details of his/her dream city and the affordable budget. 
After filling the google sheet, the IATA codes will get generated automatically with the help of kiwi partners API and will get auto filled in the google sheet using the sheety API.
Now the user will be asked to fill in the form where it will provide other necessary details like fly from, number of nights, number of adults etc and using the same kiwi partners API but using a different url endpoint the user will get all the flights those fit in its budget for a given dream city based on the above mentioned queries.
After getting the response from the API, the user’s dashboard will get filled automatically according to the response by the API and the user can select the flight of his choice.
After using our website travel bay, the user also gets an option to add a review for better user experience where user can give the rating and share his/her experience.
##Technologies Used
###Frontend
We are using Html, CSS and Bootstrap for the frontend of our website which comprises of 4 pages.
Home page – This is the main page of our website. This contains the sign-up/sign-in option and a brief description of what we do. After that, we have added a carousel using bootstrap which has 3 slides indicating the steps, the user needs to follow to get the best results.
In the end, we have a footer which has 2 buttons, one is the link to the google sheet in which the user is required to enter his/her dream destination and its budget. After that clicking on the ‘ok’ button auto fills the IATA codes for the above mentioned destinations and then redirects the user to the form page.

Form page – In the Form page, we ask the user to enter other necessary details like fly from, number of nights, number of adults etc using  kiwi partners API. On the basis of the details entered by the user, the kiwi API will generate all possible dream flights according to his/her budget which will be displayed on the dashboard page.

Dashboard page – In this page, all the details of the user’s dream flight/flights will be rendered into div cards for his/her reference. It can also contains a link to the review page wherein the user can post a review to our website for better user experience.
Review page – 
###Backend 
For Backend we used MySql command line client and MySql workbench for better GUI interface.

###Team-mates

Prateek Jain           2010110477

Anubhav Talus       2010110113

Pratham Sharma   2010110479
