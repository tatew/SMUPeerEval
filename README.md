# SMUPeerEval
BIT 4454 capstone project, spring 2021

## Starting the project
- Start Ubuntu
- `cd` to the directory where the project is saved
- run `code .`
- Open a terminal in VSCode: Terminal > New Terminal 
- Run `source ~/path/to/venv/bin/activate` Example: `source ~/.virtualenvs/SMUPeerEval/bin/activate`
- Run `git fetch`
- Run `git pull`
- Run `docker-compose up -d` to start the DB 
Now you can run the app with `plz man runserver`, connect to the db with DataGrip, etc... 

## When you're done, shut everything down
- Run `dc stop`
- Commit your changes: `git add -u`, `git add path/to/untracked/files`, `git status`, all files should be green, `git commit -m "Commit message"`, `git push`
- Run `deactivate`
- Close VSCode
- In the Ubuntu Shell, run `exit`
