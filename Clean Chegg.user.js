// ==UserScript==
// @name         Clean Chegg
// @description  Formats Chegg pages nicely
// @version      2.3
// @author       bhackel
// @homepageURL  https://github.com/bhackel/cheggbog
// @match        https://*.chegg.com/homework-help/*
// @icon         https://www.google.com/s2/favicons?domain=chegg.com
// @namespace    https://github.com/bhackel/cheggbog
// @license      MIT
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
            let ansImgLst = Array.from(document.querySelector('#chegg-main-content > div > div > div > div > div:nth-child(2) > section').querySelectorAll('img')).slice(1);
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
