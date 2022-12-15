# cheggbog

*Note that usage of this bot breaks Discord ToS and can get you banned if reported*

Fully automated Chegg Discord bot for homework help.
**Working Dec 15, 2022**

## Overview

Recently, Chegg has made it difficult to automate retrieval of content from their website. They now use a service called
**PerimeterX** that detects the usage of automation tools like Selenium when accessing the website.

This program demonstrates a way to circumvent these restrictions. It uses a virtual machine and fake keystrokes to
simulate a real user on the website.

## Requirements

- **Paid Chegg account** (will need to sign in)
- A decent computer/server to run the VM
- Basic Python skills
- A Discord bot

## Step 0: Obtaining the bot and creating the VM

Look up how to create a Discord bot, then add it to any server. The permissions required are Read and Send messages,
Attach files, and Add reactions.

Download the free **VMware Workstation 16 Player**.

Grab the **Media Creation Tool** from Microsoft's website to create a .iso of Windows. You can also grab a Linux .iso
instead, like Ubuntu. Create a new virtual machine using that .iso file and go through the setup process.

For **Windows 10** setup, click on "I don't have a product key". When prompted to sign in with a Microsoft account,
disconnect from the internet to create a local account with no password. Install VMware Tools, Chrome, and Python (
tested 3.9). Make sure to add Python to PATH when installing.

For **Ubuntu 22.04**, consider choosing the minimal installation option in the setup. Set any username and password.
Make sure to click the box to enable automatic login on startup.

## Step 1: Setting up Chrome

The bot opens the URL in Chrome, takes a screenshot using the **GoFullPage** shortcut, then sends the image in the same
channel as the link. Afterwards, it closes the tab and deletes the image.

First, download Chrome. On Ubuntu, download the .deb, and install it
using `sudo dpkg -i google-chrome-stable_current_amd64.deb`. If you are prompted for a keyring password, leave it blank
to make startup easier

Sign in to Chegg. Ensure the device is registered to the account by opening any homework-help link.

Install the **GoFullPage** extension from the Chrome web store. Right-click the icon, go to settings:

- Set Image format to `jpg`
- Set directory to `screenshots`
- Check Auto-download files
- Allow any permissions requested

### Optional (but *highly recommended*) improvements for speed and reliability

<details>
  <summary>Click to view</summary>

Install uBlock Origin to remove ads

Install Tampermonkey and add the following as a script to improve formatting

```javascript
// ==UserScript==
// @name         Clean Chegg Website
// @namespace    http://tampermonkey.net/
// @version      2.2
// @description  Formats Chegg pages nicely
// @author       You
// @match        https://www.chegg.com/homework-help/*
// @icon         https://www.google.com/s2/favicons?domain=chegg.com
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    setTimeout(function () {
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
            let thumbsDiv = document.querySelector('#chegg-main-content > div > div > div > div > div:nth-child(2) > section > div:nth-child(4) > div > div > div > div > div:nth-child(3)');
            if (thumbsDiv) {
                thumbsDiv.querySelector("div > button:nth-child(1) > div").style.color = "red";
                thumbsDiv.querySelector("div > button:nth-child(1) > div").style.fontSize = "75px";
                thumbsDiv.querySelector("div > button:nth-child(2) > div").style.color = "red";
                thumbsDiv.querySelector("div > button:nth-child(2) > div").style.fontSize = "75px";
            }

            // Click "All Steps" for pages with steps
            let button = document.querySelector('#chegg-main-content > div > div > div > div > div:nth-child(2) > section > div:nth-child(4) > div > div > div > div > div > div:nth-child(1)');
            if (button) {
                button.click(); // first, click show one step
            }
            setTimeout(function () {
                let button = document.querySelector('#chegg-main-content > div > div > div > div > div:nth-child(2) > section > div:nth-child(4) > div > div > div > div > div > div:nth-child(2)');
                if (button) {
                    button.click(); // then, click show all steps
                }
            }, 500)

            // Increase size of images when they are small for some reason
            let ansImgLst = document.querySelector('#chegg-main-content > div > div > div > div > div:nth-child(2) > section > div:nth-child(3) > div > div > div > div > div:nth-child(2)').getElementsByTagName('img')
            for (let img of ansImgLst) {
                if (parseInt(img.style.width, 10) < 600) {
                    img.style.width = '600px'
                }
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

Change the VM resolution to something like 1600x1200 in Display Settings.

</details>

## Step 2: Setting up the Discord bot

Next, install Python.

On **Ubuntu 22.04**, run `sudo apt-get install pip` to install pip. Then, run `sudo apt-get install python3-tk` for
tkinter, which is necessary for the keyboard library.

Download this repository as a zip and extract it anywhere.
Add your bot's private key to key.txt.
Open cheggbog.py and edit the "path" variable with the correct path for your system. On Linux, the path looks
like `"/home/[YOUR_USERNAME]/Downloads/screenshots/*.jpg"`

Open a command prompt or terminal in the folder and install the required libraries.

On **Windows 10**, you may need to use `py` in place of `python`. On **Ubuntu 22.04**, use `python3` in place
of `python`.

```
python -m pip install -r requirements.txt
```

Finally, run the bot

```
python -m pip install -r requirements.txt
```

**Keep at least 1 tab open while the bot is running to improve loading times**

## Step 3: Testing and final parts

Make sure to disable automatic sleep and display turnoff in the settings of your system.

When running, the bot looks for links in any channel it can see, including DMs. Send any Chegg link and do not touch the
virtual machine. The intended behavior is the following:

- Link sent, bot reacts with an emoji to show processing
- Bot opens link in Chrome, waits for a bit, then triggers the full page screenshot tool
- Once complete, bot replies to the link with image, closes the Chegg window, and deletes the image file
- Then, bot reacts to the link to indicate completion

### (Optional) Adding the bot to the VM startup

#### Windows 10

In the cheggbog folder, create a new file called run.bat with the following contents

```
python cheggbog.py
```

Press Win+R and type shell:startup to access the startup programs folder. Create a shortcut to the run.bat file and drop
it here, along with a shortcut to Chrome.

#### Ubuntu 22.04

Install gnome-startup-applications using `sudo apt-get gnome-startup-applications` if it does not exist.

In the cheggbog folder, create a new file using `touch startup.sh`. Make it executable using `chmod +x startup.sh`. Open
it in a text editor and add the following contents

```
#!/bin/bash
cd /home/[yourpathhere]/cheggbog/
python3 /home/[yourpathhere]/cheggbog/cheggbog.py
```

Open Startup Applications. Click Add. Set the name to Chrome. Set the command to google-chrome.

Click Add again. Set the name to cheggbog. Set the command
to `gnome-terminal -x bash -c "/home/[yourpathhere]/cheggbog/startup.sh"`

### (Optional) Adding the VM to the host startup

On the Windows host, navigate to the VM (default C:\Users\[User]\Documents\Virtual Machines\[Your VM]).
Create a .bat file with the following contents (substitute brackets)

```
"C:\Program Files (x86)\VMware\VMware Player\vmrun" -T player start "C:\Users\[User]\Documents\Virtual Machines\[Your VM]\[Your VM].vmx"
```

Create a shortcut to this file and place it in the shell:startup folder of the host

Thanks for reading, please leave a star if you found this tool useful, or leave an issue if it was useless.
