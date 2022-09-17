# cheggbog

*Note that usage of this bot breaks Discord ToS and can get you banned if reported* 

Fully automated Chegg Discord bot for "homework help".
**Working Jul 25, 2022**

## Overview
Recently, Chegg has made it extremely difficult to automate retrieval of content from their website. They started using a service called **PerimeterX** that detects the usage of automation tools like Selenium when accessing the website.

This program demonstrates a way to circumvent these restrictions. It uses a virtual machine and fake keystrokes to simulate a real user on the website.

## Requirements
- Paid Chegg account (will need to sign in)
- A decent computer/server to run the VM
- Basic Python skills
- A Discord bot

## Step 0: Obtaining the bot and creating the VM
Look up how to create a Discord bot, then add it to any server. The permissions required are Read and Send messages, Attach files, and Add reactions.

Download the free **VMware Workstation 16 Player**. Grab the **Media Creation Tool** from Microsoft's website to create a .iso of Windows. Create a new virtual machine using that .iso file and go through the setup process.

In setup, click on "I don't have a product key". When prompted to sign in with a Microsoft account, disconnect from the internet to create a local account with no password. Install VMware Tools, Chrome, and Python (tested 3.9.7). Make sure to add Python to PATH when installing.

## Step 1: Setting up Chrome
The bot opens the URL in Chrome, takes a screenshot using the **GoFullPage** shortcut, then sends the image in the same channel as the link. Afterwards, it closes the tab and deletes the image.

Sign in to Chegg. Ensure the device is registered to the account by opening any homework-help link.

Install the **GoFullPage** extension from the Chrome web store. Right click the icon, go to settings:
- Set Image format to jpg
- Set directory to screenshots
- Check Auto-download files
- Allow any permissions requested

### Optional (but *highly recommended*) ways to improve speed and quality
<details>
  <summary>See below</summary>

Install Tampermonkey and add the following as a script to improve formatting
```javascript
// ==UserScript==
// @name         Clean Chegg Website
// @namespace    http://tampermonkey.net/
// @version      2.1
// @description  try to take over the world!
// @author       You
// @match        https://www.chegg.com/homework-help/*
// @icon         https://www.google.com/s2/favicons?domain=chegg.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    setTimeout(function(){
        let url = window.location.href.split('?')[0];
        // Case for Q&A pages
        if (url.includes("/homework-help/questions-and-answers/")) {
            // Main page formatting
            document.querySelector("#__next > div > div > div").style.margin = 0; // Removes auto centering of content
            document.querySelector("#chegg-main-content > form").remove(); // Removes the search box at the top of the page
            document.querySelector("#__next > div > div > div > header").remove(); // Removes the title bar at the top of the page
            document.querySelector("#chegg-main-content > div > div > div:nth-child(2)").remove(); // Removes the right sidebar
            document.querySelector("#__next > div > div:nth-child(2)").remove() // Removes the footer
            document.querySelector("#chegg-main-content > div > div > div > div > div:nth-child(3)").remove(); // Removes "Up next in your courses" above footer
            document.querySelector("#__next > div > div > nav").remove() // Removes side navigation bar

            // Details
            document.querySelector("#chegg-main-content > div > div > div > div > div:nth-child(1) > section > div > div > div:nth-child(2) > div").style.maxWidth = "none"; // Allows question text to be infinitely wide
            document.querySelector("#chegg-main-content").style.padding = "5px"; // Shrinks main content padding
            document.querySelector("#chegg-main-content > div > div").style.display = "inline" // Makes content fill entire width of the page (up to a max SET BELOW)
            document.querySelector("#chegg-main-content").style.width = "960px"; // Sets the width of the main content, change this according to the width of the window

            // Makes thumbs up/down more visible
            let e = document.querySelector("#chegg-main-content > div > div > div > div > div:nth-child(2) > section > div:nth-child(3) > div > div > div > div > div:nth-child(3) > div");
            if (e) {
                e.style.fontSize = "75px";
                e.querySelector("div > button:nth-child(1) > div").style.color = "red";
                e.querySelector("div > button:nth-child(2) > div").style.color = "red";
            }

            // Click "All Steps" for pages with steps
            let button = document.querySelector('#chegg-main-content > div > div > div > div > div:nth-child(2) > section > div:nth-child(3) > div > div > div > div > div > div:nth-child(2)');
            if (button) {
                button.click();
            }
        }

        // All other (textbook answers)
        else {
            document.querySelector(".chg-footer").remove() // Removes footer
            document.querySelector(".playerpages-right-content").remove() // Removes right sidebar
            document.querySelector("div[role='navigation']").remove() // Remove search and title bar
            document.querySelector(".chg-container").style.marginLeft = "0"; // Removes auto centering of content
            document.querySelector(".chg-container").style.paddingTop = "0"; // Removes padding on top of content
            document.querySelector(".chg-content").style.paddingBottom = "0"; // Removes padding below content
            document.querySelector(".chg-content").style.margin = "5px"; // Shrinks margins between edge and page
            document.querySelector(".chg-container").style.minWidth = "unset"; // Removes horizontal scrollbar by removing minimum width restriction
            document.querySelector(".csp-content").remove(); // Removes more footer content
            document.querySelector("oc-component[data-name='opencomponent-relatedcontent']").remove() // Removes related content section
            document.querySelector(".main").style.paddingBottom = "unset"; // Shrinks padding at bottom
            document.querySelector("div[id='solution-player-sdk']").style.marginBottom = "unset"; // Shrinks margin at bottom
            document.querySelector(".chg-container").style.minHeight = "unset"; // Shrinks total page height
            document.querySelector(".global-breadcrumb").style.width = "775px" // Forces breadcrumb text to certain width

        }

    }, 3000) // Increase this delay for slower internet connections and page loading times

})();
```

Change the VM resolution to something like 1600x1200 in Display Settings in Windows

</details>

## Step 2: Setting up the Discord bot
Download this repository as a zip and extract it anywhere. Add your bot's private key to key.txt. 
Open cheggbog.py and edit the "path" variable with your Windows username.

Open a command prompt in the folder and install the required libraries
```
python -m pip install -r requirements.txt
```

Finally, run the bot
```
python cheggbog.py
```
**Keep at least 1 tab open while the bot is running to improve loading times**

## Step 3: Testing and final parts
When running, the bot looks for links in any channel it can see, including DMs. Send any Chegg link and do not touch the virtual machine. The intended behavior is the following:
- Link sent, bot reacts with an emoji to show processing
- Bot opens link in Chrome, waits for a bit, then triggers the full page screenshot tool
- Once complete, bot replies to the link with image, closes the Chegg window, and deletes the image file
- Then, bot reacts to the link to indicate completion

### (Optional) Adding the bot to startup
In the cheggbog folder, create a new file called run.bat with the following contents
```
python cheggbog.py
```
Press Win+R and type shell:startup to access the startup programs folder. Create a shortcut to the run.bat file and drop it here, along with a shortcut to Chrome.

### (Optional) Adding the VM to startup
On the host, navigate to the VM (default C:\Users\[User]\Documents\Virtual Machines\[Your VM]).
Create a .bat file with the following contents (substitute brackets)
```
"C:\Program Files (x86)\VMware\VMware Player\vmrun" -T player start "C:\Users\[User]\Documents\Virtual Machines\[Your VM]\[Your VM].vmx"
```
Create a shortcut to this file and place it in the shell:startup folder of the host



Thanks for reading, please leave a star if you found this tool useful, or send me a message if it was useless.
