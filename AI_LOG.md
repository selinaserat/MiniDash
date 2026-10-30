# MiniDash — AI Interaction Log

**Project:** MiniDash — Track C: Live Order Tracking  
**AI Tool:** ChatGPT  
**Development Environment:** Python, FastAPI, SQLite, PyCharm, GitHub  
**Date:** October 2026

For this project, I used ChatGPT to help me understand how to build certain parts of MiniDash, troubleshoot errors, and check my work. I didn't just copy the code and assume everything would work. I ran the application, tested the features, and went back to fix things when something wasn't working correctly.

I didn't record the exact time of every interaction, so I organized this log by the parts of the project I was working on.

## Entry 1 — Setting Up the Project

**What I asked:** I asked ChatGPT to help me start my MiniDash project using FastAPI and SQLite.

**What AI suggested:** It gave me starter code, explained how to organize my files, and helped me set up the database and Git.

**What I did:** I created the project in PyCharm, followed the setup instructions, and checked that the application and database were working.

**Result:** I had the basic structure of my project ready so I could start adding features.

## Entry 2 — Requirements and Architecture

**What I asked:** I needed help organizing the requirements and planning how the application would work.

**What AI suggested:** ChatGPT helped me break the project down into smaller parts and organize the documentation.

**What I did:** I reviewed the suggested structure and added the documentation to my project.

**Result:** I had a clearer idea of what needed to be built and how the different parts would connect.

## Entry 3 — Fixing Database Issues

**What I asked:** I ran into database connection warnings while working on my tests and asked ChatGPT what they meant.

**What AI suggested:** It explained possible issues with how SQLite connections were being handled and suggested changes.

**What I did:** I updated the code and continued running my tests to make sure I hadn't broken anything.

**Result:** I was able to continue working with the database and testing the application.

## Entry 4 — Creating Orders and Updating Their Status

**What I asked:** I wanted customers to be able to place orders and track them through the delivery process.

**What AI suggested:** It helped me implement the order endpoints and the logic for moving orders between different statuses.

**What I did:** I tested creating orders and updating their statuses using the FastAPI documentation page.

**Result:** Orders could move through PLACED, PREPARING, READY, PICKED_UP, and DELIVERED.

## Entry 5 — Writing and Running Tests

**What I asked:** I asked ChatGPT for help testing the different parts of MiniDash.

**What AI suggested:** It helped me work on automated tests for restaurant information, orders, and tracking behavior.

**What I did:** I ran the tests in the PyCharm terminal and worked through the issues until they passed.

**Result:** I ended up with 21 passing automated tests.

## Entry 6 — Git and GitHub

**What I asked:** I needed help keeping track of my changes and uploading my work to GitHub.

**What AI suggested:** It explained how to use commands like `git add`, `git commit`, `git push`, and `git status`.

**What I did:** I ran the commands myself, checked the terminal output, and made sure the changes were uploaded.

**Result:** My project was saved in GitHub with a history of my commits.

## Entry 7 — Building the Website

**What I asked:** Once the backend was working, I wanted MiniDash to have an actual website instead of only using the API documentation. I wanted something similar to a food delivery website.

**What AI suggested:** ChatGPT helped me create the HTML, CSS, and JavaScript for displaying restaurants, menus, a shopping cart, and order tracking.

**What I did:** I created the frontend files in PyCharm and connected them to my FastAPI backend.

**Result:** I could open MiniDash in my browser and interact with the website.

## Entry 8 — Fixing the Menu Display and Prices

**What I asked:** When I tested the website, I noticed that some of the food images didn't make sense. For example, pasta was showing a burger emoji. I also noticed that some prices were showing `$NaN`.

**What AI originally gave me:** The JavaScript wasn't properly matching food items to their display icons, and it was using the wrong field for the prices.

**What I changed:** I didn't want to keep the original version because it looked incorrect. I asked ChatGPT to change the food displays and fix how the prices were being read from the backend.

**How I checked it:** I refreshed the website and checked the menu again.

**Result:** The menu looked more accurate and the price problem was corrected.

## Entry 9 — Fixing Checkout

**What I asked:** When I tried placing an order, I received an error because the delivery address was missing.

**What AI suggested:** ChatGPT explained that the backend required an address when creating an order and suggested adding an address prompt.

**What I did:** I updated the checkout process and tried again using a test address.

**Result:** I was able to place an order successfully.

## Entry 10 — Fixing Live Tracking

**What I asked:** After placing an order, the tracking section displayed a "Method Not Allowed" error.

**What AI originally gave me:** The JavaScript was requesting `/orders/{order_id}/status`, which wasn't the correct endpoint for retrieving tracking information.

**What I changed:** I checked the available endpoints in FastAPI's documentation and found that the correct one was `/orders/{order_id}/tracking`. I replaced the incorrect request instead of keeping the original code.

**How I checked it:** I placed another order and watched the tracking section.

**Result:** The tracking information started displaying correctly, and the status updated when I changed it through the API.

## Entry 11 — Testing Invalid Order Statuses

**What I asked:** While testing the order statuses, I received a 422 error and wasn't sure why.

**What AI explained:** It pointed out that I had entered `PINKED UP` instead of `PICKED_UP`, and the status needed to match the allowed value exactly.

**What I did:** I corrected the value and continued updating the order through the remaining delivery stages.

**Result:** I confirmed that the application rejects invalid status values and that I could complete the order through DELIVERED.

## Entry 12 — Final Testing and GitHub Upload

**What I asked:** I wanted to make sure my project was saved properly and everything was working before submission.

**What AI suggested:** ChatGPT gave me commands to check my GitHub status and run the automated tests again.

**What I did:** I ran the tests and confirmed that all 21 passed. I also pushed my latest changes to GitHub.

**Result:** The latest frontend changes were committed as `4a91d38`. Git showed that my branch was up to date and there was nothing left to commit.

## What I Learned

Using ChatGPT helped me get through parts of the project that I wasn't completely familiar with, especially connecting the frontend to the backend and understanding the errors.

One thing I realized is that AI-generated code doesn't always match what is already in the project. The price issue and the tracking endpoint issue were both examples of that. The code looked reasonable at first, but when I actually ran it, it didn't work correctly.

I had to explain the errors, look at the API documentation, make changes, and test everything again.

Overall, AI was helpful for figuring out what to try next, but I still had to verify that the code worked in my actual application.
