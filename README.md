# LibrePasswordListGenerator

[watch this video to learn why you need to use this program](https://www.youtube.com/watch?v=7U-RbOKanYs)

![screenshot of the program](http://i.imgur.com/E5Eoiwc.png "screenshot of the program")

this is a Libre(free as in freedom) password generator which generates a list of passwrd based on a master password, then keeps track of what sites these passwords are for(but the passwords are always generated and thus never stored anywhere) then it helps you keep track of which password is for which site.
also, this application's sourcecode is simple enough that it can easily be peer reviewed, so you do not need to worry the passwords of websites are sent to an malevolent party.

dependencies:

pytnon 2.X python-tk

on linux **(debian variants)** do:

`sudo apt-get install python python-tk`

`pytnon LibrePasswordListGenerator.py`

on windows download and install pytnon 2.X**(have only tested it on Linux yet)**

start powershell type the full path to python then space and the full path to LibrePasswordListGenerator.py

example:

`c:\python\bin\python.exe c:\downloads\LibrePasswordListGenerator.py`

on mac it should just work**(have only tested it on Linux yet)**

on terminal go to the directory where LibrePasswordListGenerator.py is at

example:

`cd ~/Downloads`

`python LibrePasswordListGenerator.py`

when prompted for your master password enter anything as your password, remember it is better if this is a safe password too
