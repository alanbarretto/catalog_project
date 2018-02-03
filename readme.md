# Udacity FSND Project 4: Item Catalog Project

This is the third major project in Udacity's Full Stack Nanodegree Course which features lessons in python, sqlalchemy, and Flask.  The goal is to create an app that allows users to Create, Read, Update, and Delete data.  It also features third party authentication such as OAuth. 
About the App: Joe’s Used Car Lot

The App “Joe’s Used Car Lot” allows users who are logged in to post their vehicles for sale.  It can be posted in one of the numerous categories, or a user can create an exclusive space called a “garage” where all their vehicles can be posted in one place. 
However, vehicles posted in garages will also show up in the appropriate categories.  So, if a user creates a garage and posts an SUV there, potential buyers will find that vehicle in that garage as well as in the SUV category.

## Getting Started

To run the app, you'll use a virtual machine (VM) which is a Linux system server that runs on top of your own machine.

You will have to download Virtual Box from this link https://www.virtualbox.org/wiki/Downloads. Virtual Box is the software the runs the virtual machine (VM).
Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

After that, you need to download Vagrant, which is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. https://www.vagrantup.com/downloads.html

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

## How to Use Virtual Box

Using the terminal, change directory to the folder containing the VM files. Then, change directory to the vagrant subdirectory. From there, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When it is done, you will get your shell prompt back. This time, type vagrant ssh to log in to your newly installed Linux VM!

Once you get vagrant up, you need to navigate to the project directory by typing cd /vagrant/catalog_project

## Using the App

Open a browser window and type in http://localhost:5000

This will bring you to the homepage where you will see the different categories of vehicles.  Below the categories are the different garages that have been created by other users.  

You can explore the whole App while not being logged in.  You can enter any category or any garage and check out the details of any of the vehicles posted there.  However, you cannot post a vehicle to sell, have administrative powers over the vehicles, or contact the seller of the vehicles that you are interested in purchasing.  

Click on the login link and you will be asked to do a third-party authorization through either your google or facebook account.  If you don’t have either, simply create one.  It’s free!

Once you are logged in, you will have the ability to post a vehicle to sell in any of the categories, create a garage of your own and post vehicles in it. You will also be able to edit and/or delete any of the vehicles and/or garages that belong to you. 

Keep in mind that you can only edit and delete vehicles and garages that you have created. 

Don’t forget to log out when you’re done.

## Limitations:

The feature to upload pictures for the vehicles and garages is not yet available.  Pictures will be replaced by a placeholder from placehold.it

## Known Bugs

It would be best to use a fresh incognito window if you are using Google Chrome to avoid caching issues.  If you use other browsers, you may have to clear cookies every time you log out and log back in.




