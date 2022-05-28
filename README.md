LIBRARY MANAGEMENT SYSTEM API
## Overview
This Library management system API allows users to sign in and have access to a catalogue of books. The books is made available for rental or unavailable if already rented. 
The Librarian is the sole person that has Admin rights to the system. Their role will be to add librarians and generate an alphanumeric password for them. The password, together with their email will be used to sign into the system. On getting a password, a librarian is required to change the default password handed them by the authorising librarian. 
Ordinary users sign up into the system either with their email and password or through social authentication(google’s OAuth only). A user can request a book, and this is either approved or disapproved of by the librarian. Once a request is approved, that book becomes unavailable to other users until it is returned by the borrower. They also must return the book at the right time. 
When a book is due for return and it is not yet returned, set the user to be inactive for a month, starting from the day of expiry.

## Librarian Roles
This project is a library management system, where a librarian can have the following privilages
1. Sign in into the system
2. Add books to catalogues
3. Add other Librarians and remove users (Both Librarians and Ordinary Users)
4. Approve and disapprove of book rental request
5. Deactivate borrowers
6. Add, update, and delete a book from a catalogue
7. Approve Book returns

## Ordinary users roles:
1. Signup to the system both socially and traditionally.
2. Change their password
3. Request a book
4. Return a book


## Installation steps

1. Ensure you have python3 installed

2. Clone the repository
3. create a virtual environment using `virtualenv venv`
4. Activate the virtual environment by running `source venv/bin/activate`

- On Windows use `source venv\Scripts\activate`

5. Install the dependencies using `pip install -r requirements.txt`

6. Migrate existing db tables by running `python manage.py migrate`

7. Run the django development server using `python manage.py runserver`


