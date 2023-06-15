A create-react-app that is modern, elegant, mobile-responsive and styled with bootstrap css, offering a simple form to RSVP to a Christmas party. The project is started through npm start so make sure theres a corresponding package.json file. This app has 3 sections.

#### 1: The hero header: RSVP Form
Form has following fields: first name, last name, checkbox indicating a +1 that the guest would like to bring to the party. All of the form elements are styled with bootstrap css. This section has a low-opacity background image of a christmas tree sourced from unsplash api or similar. 

When the user hits submit, the form payload is written to a local json file titled data.json. 

#### 2: Attending List (table)
Below the form, render a beautiful list of all the guests who have RSVP'd, with their first name, last name, and whether they are bringing a +1. The table is generated from the data.json file.
This table should be sortable by first name and last name, and uses bootstrap for styling.

#### 3: Costume Contest and Gift Exchange
Pulls a random pokemon from the pokemon api and suggest that the user dress up as that pokemon for the costume contest. Also, randomly assign the user a gift exchange partner from the list of guests who have RSVP'd in data.json. 

Make sure the app includes the links to bootstrap cdn and jquery cdn in the index.html file.