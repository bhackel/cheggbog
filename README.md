# cheggbog
Fully automated Chegg Discord bot for "homework help".
**Working Sept 15, 2021**

## Overview
Recently, Chegg has made it extremely difficult to automate retrieval of content from their website. They started using a service called **PerimeterX** that detects the usage of automation tools like Selenium when accessing the website.

I still wanted to automate the process, so I took it to the extreme with this project. It uses a virtual machine and fake keystrokes to simulate a real user on the website.

## Requirements
- Paid Chegg account (will need to sign in)
- A decent computer to run the VM
- Basic Python skills
- A Discord bot

## Step 0: Obtaining the bot and creating the VM
Look up how to create a Discord bot, then add it to any server. It needs the permissions to read messages and add reactions.

For the virtual machine, I am using **VMware Workstation 16 Player**. It's free and works well. Once it is installed, grab the **Media Creation Tool** from Microsoft's website, and use it to create a .iso of Windows. Create a new virtual machine using that .iso file, and go through the setup process.

For the VM, click on "I don't have a product key". When it asks you to sign in with a Microsoft account, you can disconnect from the internet, which allows for the creation of a local account and having an empty password. Then, you'll want to install VMware Tools, Chrome, and Python (tested on version 3.9.7). Make sure to check the box to add Python to PATH when installing.

## Step 1: Setting up Chrome
The way the bot works is that it opens the URL in Chrome, takes a screenshot of it using the **GoFullPage** extension by pressing a shortcut for it, then sends that image in the channel where the Chegg link was sent. The tab is also closed and the image is deleted once it is done.

Go to the Chegg website and sign in. Make sure that the device is registered to your account by going to any homework-help link.

Install the **GoFullPage** extension from the Chrome web store. Right click the icon, go to settings:
- Set Image format to jpg
- Set directory to screenshots
- Check Auto-download files
- If it asks for permissions, make sure to allow it

### Optional (but recommended) tools to improve image output
<details>
  <summary>See below</summary>
  
Install uBlock Origin and add the following as a filter to trim useless page information
```
! 2021-09-10 https://www.chegg.com
www.chegg.com##.loggedIn.subtype-.type-study.kit-kat-search.force-desktop.chgg-hdr
www.chegg.com##.header-nav.no-subnav.no-nav.chg-body > div > oc-component
www.chegg.com##.sidebar-container
www.chegg.com##.right-sidebar
www.chegg.com##.csrec-cards.csrec-qna
www.chegg.com###playerpages-right-content
www.chegg.com##.playerpages-right-content.col-3
```

Install Tampermonkey and add the following as a script to improve formatting
```javascript
// ==UserScript==
// @name         Clean Chegg Website
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  try to take over the world!
// @author       You
// @match        https://www.chegg.com/homework-help/questions-and-answers/*
// @icon         https://www.google.com/s2/favicons?domain=chegg.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    document.querySelector("div.chg-container.center-content").style.maxWidth = "calc(100% - 13px)";
    document.querySelector("div.chg-container.center-content").style.padding = "0";
    document.querySelector("div.chg-container.center-content").style.margin = "0";
    document.querySelector("div.main-content.question-page").style.width = "calc(100% - 13px)";
    document.getElementById("popup-4").style.paddingBottom = "0";
    document.querySelector("div.chg-footer").style.display = "none";
    document.querySelector('div.txt-2-small.global-breadcrumb').style.display = "none";
    document.querySelector('div.parent-container.question-headline').style.paddingTop = "0";
    document.querySelector('div.parent-container.question-headline').style.paddingBottom = "0";
    document.querySelector('div.main-content.question-page').style.width = "100%";
    document.querySelector('div.chg-content.HomeworkhelpQuestion').style.padding = "0";
    document.querySelector('div.chg-content.HomeworkhelpQuestion').style.minWidth = "unset";
})();
```

Change the VM resolution to something like 1600x1200 in Display Settings in Windows

In Chrome, set a default resolution by right clicking on the empty space next to the tabs and clicking Size (unsure if this works).

</details>

## Step 2: Setting up the Discord bot
Download this repository as a zip and extract it to anywhere. Add your bot's private key to key.txt. 
Open cheggbog.py and edit the variable called "path" with your username.

Open a command prompt in the folder and install the required libraries using the following
```
python -m pip install -r requirements.txt
```

Then you can run the bot by typing the following command
```
python cheggbog.py
```
**Make sure to have at least 1 tab open while the bot is running to improve loading times**

## Step 3: Testing and final parts
When the bot is running, it is looking for both DMs and messages sent in any channel it can see. Send any Chegg homework help link and make sure not to touch the virtual machine. The intended behavior is the following:
- Link sent, bot reacts with an emoji to show processing
- Bot opens link in Chrome, waits for a bit, then triggers the full page screenshot tool
- After a set amount of time, the bot sends the image in the same channel as the link, closes the Chegg window, and deletes the image file
- Finally, reacts to the original message to show that it is complete

### (Optional) Adding the bot to startup
In the cheggbog folder, create a new file called run.bat with the following contents
```
python cheggbog.py
```
Press Win+R and type shell:startup to access the startup programs folder. Create a shortcut to the run.bat file and drop it in this folder, along with a shortcut to Chrome.

### (Optional) Adding the VM to startup
On the host computer, go to the location of the VM (default C:\Users\[User]\Documents\Virtual Machines\[Your VM]).
Create a .bat file with the following contents (substitute things in brackets)
```
"C:\Program Files (x86)\VMware\VMware Player\vmrun" -T player start "C:\Users\[User]\Documents\Virtual Machines\[Your VM]\[Your VM].vmx"
```
Create a shortcut to this file and place it in the shell:startup folder of the host



Thanks for reading, please leave a star if you found this tool useful, or send me a message if it was useless.
