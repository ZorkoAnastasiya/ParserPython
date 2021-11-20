# ParserPython  [![View project](https://img.shields.io/badge/VIEW-PROJECT-BD51B9)](https://parser-py.herokuapp.com/)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1A52B5?style=flat&labelColor=D4A70D)](https://www.python.org/)
[![mypy](https://img.shields.io/badge/checked_by-mypy-000000?style=flat&labelColor=18B51A)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

[![GitHub commits](https://badgen.net/github/commits/ZorkoAnastasiya/ParserPython)](https://github.com/ZorkoAnastasiya/ParserPython/commit/)
[![GitHub latest commit](https://badgen.net/github/last-commit/ZorkoAnastasiya/ParserPython)](https://github.com/ZorkoAnastasiya/ParserPython/commit/)
[![Lines of code](https://img.shields.io/tokei/lines/github.com/ZorkoAnastasiya/ParserPython)](https://github.com/ZorkoAnastasiya/ParserPython)
---

### _Technologies:_

[![pycharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)](https://www.jetbrains.com/ru-ru/pycharm/)
[![heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://devcenter.heroku.com/categories/reference)
[![django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://docs.djangoproject.com/en/3.2/)
[![beautiful soup](https://img.shields.io/badge/Beautiful_Soup-0D6E6E?style=for-the-badge&Color=white)](https://www.crummy.com/software/BeautifulSoup/)
[![httpx](https://img.shields.io/badge/HTTPX-FFDFEB?style=for-the-badge&Color=white)](https://www.python-httpx.org/)
[![postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

---

### _About the project:_

__ParserPython__ is a tutorial project designed to learn how to parse data, store and present that data using __Django__ framework technologies.

---

### _The project is a website with the following functions:_

* registration and authorization of users;
* getting a list of news from supported resources;
* receiving the text of a specific news;
* update of previously saved articles;
* transition to the original source of news;
* adding links to another resource and receiving data from the specified address;
* creation of your own news archive, with the ability to add or remove articles from it.

---

### _Installing and running the project:_

1. Install packages from requirements.txt file
2. Set the environment variable DEBUG (True - for local launch)
3. Add the environment variable DATABASE_URL, indicating the url to the connected database
4. Run the following commands from the superproject directory:

    - Apply migrations
        ```
        python manage.py migrate
        ```
    - Create a superuser for access to project administration (the project configuration is set to Russian)
        ```
        python manage.py createsuperuser
        ```
    - Start the local server
        ```
        python manage.py runserver
        ```
---	
