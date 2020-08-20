# ContactsBook:
Let me start by saying I am not a web developer. Anyway do not forget the fact once a wise man said "No matter how bad you are, you are not useless. You can still be used as a **bad example**." Now its upon you to decide to go through this project or not.

I was tasked with creating a central managed address book that can be accessed via web, so I came up with this idea of creating an interface for Google Contacts as the client did want to assign users who could use the system to update/amend/insert/delete the contacts respectively. And assign permissions accordingly for users who can edit and only view the contacts. 

Now you would be asking me why not use Google Contacts directly? Simple answer they do not have GSuits i.e. they cannot delegate access to others.

## Important libraries used by the application and what they do:
The application makes use of aiohttp as a web server i.e. aiohttp_jinja2 to render html templates. The web application also makes use jQuery and JavaScript to deal with a lot of dynamic fetching/loading of data from server, for such client to server communications it makes use of wsrpc-aiohttp. The server fetches data from Google People API therefore none of contact data are saved locally on the host. It also uses TinyDB to store the details of users who has access to the application. Passwords are not saved on the DB but the password hash - to generate password has it makes use of passlib.

## Cloning & Run:
1. `git clone https://github.com/eyaadh/contactsBook.git`, to clone and the repository.
2. `cd book`, to enter the directory.
3. `pip3 install -r requirements.txt`, to install dependencies/requirements.
4. Create a google developer project and enable Google People API. Also add `contacts` to Scopes.
> More details on Google People API and how to create the project can be found here [here](https://developers.google.com/people/v1/getting-started).
5. download OAuth Client ID file and place at `book/working_dir/credentials.json`
> More details on OAuth 2.0 to Access Goole API can be found [here](https://developers.google.com/identity/protocols/oauth2).
6. Run with `python3.8 -m book`, stop with <kbd>CTRL</kbd>+<kbd>C</kbd>.
7. Finally to access the web interface browse to `http://localhost:8080`.
```
Default Credentials:
Username: admin
Password: password

Username: user
Password: password1
```