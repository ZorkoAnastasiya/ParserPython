# ParserPython

##### _About the project:_

__ParserPython__ is a tutorial project designed to learn how to parse data, store and present that data using __Django__ framework technologies.

---

##### _The project is a website with the following functions:_

* registration and authorization of users;
* getting a list of news from supported resources;
* receiving the text of a specific news;
* update of previously saved articles;
* transition to the original source of news;
* adding links to another resource and receiving data from the specified address;
* creation of your own news archive, with the ability to add or remove articles from it.

---

##### _Applied technology stack:_

* _Python_
* _HTML_
* _Django_
* _BeautifulSoup_
* _httpx_
* _PostgreSQL_

---

#####_Installing and running the project:_

1.  Create a virtual environment
2. Install packages from requirements.txt file
3. Set the environment variable DEBUG (True - for local launch)
4. Add the environment variable DATABASE_URL, indicating the url to the connected database
5. Apply migrations
   ```
    python manage.py migrate
   ```
6. Create a superuser for access to project administration (the project configuration is set to Russian)
   ```
    python manage.py createsuperuser
   ```
7. Start the local server
   ```
    python manage.py runserver
   ```
---	