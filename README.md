# The Coaching Manual Technical Test

## Brief
Build a registration system which consists of:  
- A HTML front end that gathers the following user data; first name, last name, email address, ISO country code  
- A RESTful API to register user data which calls an external API to gather price information and stores user data and provided price information  
- A page which lists all registered users and available plans

## Build instructions

- Install Python >=3.6

- Install a virtualenv and activate

```bash
virtualenv --no-site-packages -p python3 venv
source venv/bin/activate
```

- Clone the repo inside your virtualenv 

```bash
git clone git@github.com:Bartlett-Christopher/coaching_manual.git
cd coaching_manual
```

- Install the project requirements
```bash
pip install -r requirements.txt
```

- Migrate the db.sqlite3 database
```bash
python manage.py migrate
```

- Create a site superuser, provide username, email and password
```bash
python manage.py createsuperuser
```

- Run the project
```bash
python manage.py runserver
```

- Create a register API key  
Navigate and login to the site admin using your superuser credentials
`localhost:8000/admin`  
Add a new API key under the API key permissions section  
Provide a name for your key and save.
Make a note of the API key and store is safely, this appears at the top of the page.  

- Back in in the terminal  
Close the project server `CONTROL-C` and save the API key just generated as an environment variable under the key 'API_KEY'
```bash
export API_KEY='******'
```

- Restart the site server using the `runserver` command

- You're now all up and running :)  
Navigate to localhost:8000 to register user data.  
Navigate to localhost:8000/list to see all the registered users

## License
[MIT](https://choosealicense.com/licenses/mit/)