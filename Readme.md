<h1 align="center">spampheus</h1>
<h3>he be spamming fr fr</h3>

---
<h4>About:</h4>
Spampheus is a bot made to manage other bots to send client requests through slack api to spam a user repeatedly, This project was not made with the purpose of harm but purely for educational purposes. This started as a dare between me and a couple of my friends to see who would make the best spam bot possible and so far.. i won. This bot works by controlling multiple bots at once bypassing the rate limit of slack api entirely in theory it could scale infinitely (or as long as you're not ip banned lol), This bot was also made to participate in hackclub siege really excited to take part of that!
---
<h4>Features</h4>
Now here's the good stuff you really care about lol
<br>
The bot comes with 2 main commands one used for "Spam" and one for managing
<br>
* `/spell` is used for spam it takes in one parameter which is user id
<br>
<i>example usage: `/spell U07ES48RES3` </i>
* `/spset` is used for managing the slack bot generally it comes with a couple commands (max, channels, phrases, spam_api_keys, set_delay) to learn more use `/spset help`.
---
<h4> So you're evil? How to run this yourself </h4>
First off please don't run this yourself you could end up with a ban and actually using this is against slack TOS so please reconsider<br>

---
<h5>So you still want to run this?</h5>
Well I really can't stop you I guess... But what I can do is help you :D<br>
First off I'm not responsible for what you do nor will I ever be Secondly...<br>
To start off you're going to want to clone the repo don't know how here to help <br>
Assuming you have git (if you don't please download it)
run the following in your terminal
```angular2html
git clone "https://github.com/Nullskulls/spampheus"
```
Afterward cd into the directory and run to install the python slack libraries you need
```angular2html
pip install -r requirements.txt
```
then cd into `/Source` and run
```angular2html
python main.py
```
if this is your first time running the bot it should exit after creating `config.json` run the following command and configure it
```angular2html
nano config.json
```
after configuring run the bot again and it should work!
```angular2html
python main.py &
```