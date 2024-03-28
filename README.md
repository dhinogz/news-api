# News Site Project

## How to use the client
### Set up
In order to set the client up, we have to initialise a virtual environment and install all required packages. Use your virtual environment manager of choice, I'll be using venv

Create a virtual environemnt named .venv
```sh
$ python -m venv .venv
```

Initialise virtual environment
```sh
$ source .venv/bin/activate
```

Install requirements
```sh
$ pip install -r requirements.txt
```

Once that's done we can start running our CLI!

This is how you run the program. It displays a help page, by default.
```sh
$ python main.py
```

This will output:
```
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                                                                                             
                                                                                                                                                                                        
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help                                                       Show this message and exit.                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ delete     Deletes given story. This requires the user to be logged in.                                                                    │
│ list       Prints out the agency registry.                                                                                                 │
│ login      Logs in to a specific service given by the user. This will create a session.text file with the service's URL and session token. │
│ logout     Logs user out. This deletes the session.txt file.                                                                               │
│ news       Fetch news from a specific agency or from a random sample (20 agencies)                                                         │
│ post       Prompts user for a new story to be sent to current service saved in session.txt. This requires the user to be logged in.        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Access project live in production
https://sc23dhg.pythonanywhere.com

## Module leader info
*Admin and Author*
Username: ammar
Password: ammar123

## Demo of the project

### Login to personal news service
```sh
$ python main.py login https://sc23dhg.pythonanywhere.com/

# Prompted...
Username: admin
Password: admin_password
```

Output
```
session.txt file created with auth details
successful login
```


### Get news from various news services
```sh 
$ python main.py news
```

Output
```
┌───────────┬────────────┬───────────┬────────────┬───────────┬──────────┬────────┬───────┐
│ KEY       │ HEADLINE   │ DATE      │ AUTHOR     │ DETAILS   │ CATEGORY │ REGION │ CODE  │
├───────────┼────────────┼───────────┼────────────┼───────────┼──────────┼────────┼───────┤
│ 2c409714… │ Cushty     │ 14/03/20… │ ammar      │ The best  │ pol      │ uk     │ JRF01 │
│           │ News story │           │            │ news      │          │        │       │
│           │            │           │            │ story     │          │        │       │
│           │            │           │            │ ever      │          │        │       │
│ 65658489… │ Bitcoin    │ 14/03/20… │ ammar      │ Bitcoin   │ pol      │ uk     │ JRF01 │
│           │ crash      │           │            │ hits      │          │        │       │
│           │            │           │            │ record    │          │        │       │
│           │            │           │            │ low       │          │        │       │
│ e1fc163c… │ Test       │ 14/03/20… │ ammar      │ Testy     │ tech     │ w      │ JRF01 │
│           │            │           │            │ test test │          │        │       │
│ 2         │ Federer    │ 28/02/20… │ Alex       │ Federer   │ pol      │ eu     │ ATR02 │
│           │ New Swiss  │           │ Redshaw    │ announced │          │        │       │

and so on...

```


### Get news from one specific agency using their code and add filters, such as region and category
``` sh
$ python main.py news --cat tech --reg uk --id DHG00
```

Output
```
┌─────┬─────────────┬────────────┬─────────────┬──────────────┬──────────┬────────┬───────┐
│ KEY │ HEADLINE    │ DATE       │ AUTHOR      │ DETAILS      │ CATEGORY │ REGION │ CODE  │
├─────┼─────────────┼────────────┼─────────────┼──────────────┼──────────┼────────┼───────┤
│ 166 │ Local       │ 28/03/2024 │ Jose        │ Recent       │ tech     │ uk     │ DHG00 │
│     │ Events      │            │ Martinez    │ developments │          │        │       │
│     │ Update      │            │             │ in           │          │        │       │
│     │             │            │             │ parliamenta… │          │        │       │
│     │             │            │             │ negotiation… │          │        │       │
│ 182 │ Local       │ 28/03/2024 │ Daniel Hart │ Rain         │ tech     │ uk     │ DHG00 │
│     │ Events      │            │             │ expected in  │          │        │       │
│     │ Update      │            │             │ the region   │          │        │       │
│     │             │            │             │ tomorrow.    │          │        │       │
│     │             │            │             │ Stay         │          │        │       │
│     │             │            │             │ prepared!    │          │        │       │
│ 186 │ From the    │ 28/03/2024 │ Super User  │ This comes   │ tech     │ uk     │ DHG00 │
│     │ CLI!        │            │             │ live! From   │          │        │       │
│     │             │            │             │ the CLI!     │          │        │       │
│     │             │            │             │ Amazing what │          │        │       │
│     │             │            │             │ technology   │          │        │       │
│     │             │            │             │ can do these │          │        │       │
│     │             │            │             │ days.        │          │        │       │
└─────┴─────────────┴────────────┴─────────────┴──────────────┴──────────┴────────┴───────┘
```
