### Hitwicket Autobidder

Wrote and used these scripts to become the highest net worth team (XORs) in the [Hitwicket](https://hitwicket.com/) game world wide, and also tied for the top spot in the premier.

Scripts to Autobid on worthy players in the market for set amounts (need musketeer plan in Hitwicket).

Disclaimer: This repo is for informational and educational purpose only.

Caution
- You may have to manage lots of players in your team - potentially near 100 - their 
  form/ training etc. if you go with this approach to the game. Do it only if you can handle it.
- Judge the market conditions and use this after assessing the demand/ supply situation. 
- This can also be used to create artificial demand at your will depending on site traffic. Think.

Steps:

- Add cookies for script to run in conf files. You can get these from browser. I have removed these from git history in this repo using [bfg-repo-cleaner](https://rtyley.github.io/bfg-repo-cleaner/) and `git filter-branch`.

- Take html from ajax requests of auction filter page, paste in `auction_page.html` (taking html can be automated using [snippets](https://developers.google.com/web/tools/chrome-devtools/javascript/snippets) in chrome dev tools)

- run extract links script on html to get player links in text file, and then the autobid script (set amount before running). Run whichever bidding type 1/2 you think suits the situation.
