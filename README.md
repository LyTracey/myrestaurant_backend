# **Moonlight Cafe**

Description: A website for small cafe owners.

The deployed version of this website can be found at [here](https://www.tea-ly.co.uk).

> **NOTE:** This repository is for the backend only. Visit [frontend](https://github.com/LyTracey/myrestaurant_frontend) to view the repository for the frontend of this project.

---

## **Contents**

- [Purpose](#purpose)

- [Tech Stack](#tech-stack)

    - [Backend](#backend)

    - [Frontend](#frontend)

- [Features](#features)

    - [Design](#design)

    - [Security](#security)

    - [Pages](#pages)

- [Run on Docker](#run-locally-with-docker)

- [Feedback](#feedback)

---

## **Purpose**

I built this website to develop my full-stack engineering skills. I chose the perspective of managing and running a small cafe shop as a real-world scenario to develop my use cases around. Please note that this Moonlight Cafe is a fictitious cafe!

I developed this website around these main use cases:
> As a manager, I would like to have an overview of the cafe's sales, revenue, profits, and be warned of anything that's out of stock.

> As a sales staff member, I require an application I can use to record orders. I also need an overview of the cafe's sales and be warned of anything that's out of stock.

> As a chef, I need to be able to edit the menu as I curate the menu and need to be able to manage the inventory.

Please note these are made up use cases as I do not have any experience running or managing a cafe.

---

## **Tech Stack**
 
### Backend

The backed was built using Django and Django Rest Framework (DRF) connected to a MySQL database. I opted to use DRF wherever possibe as it provides many useful classes that abstracts Django for many common use cases applicable to this project.

The image below depicts the relationships between the user-defined models of the backend.

![image](md-images/erd.png)


Based on functionality, I split the Django backend into two apps: the users app to manage users and their authentication (named `user_app`) and the cafe app (named `myrestaurant_app`), which relates to the operating data of a cafe.


### Frontend

The frontend was built using React.js, TypeScript, React-Bootstrap, and SCSS. 

Packages of note used in this project 

---

## **Features**

### Design

The design theme of this website and cafe is day and night. Select whichever them  you like best using the theme toggle in the navbar.

### Security

<ins>Authentication</ins>

For 'non-public' pages, JWT is used to authenticate users in the backend, developed using the `Simple JWT` package ([Simple JWT]: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).

For the frontend, access and refresh tokens are stored in localStorage. Although this is vulnerable to XSS (cross-site scripting) attacks, refresh tokens are rotated (new refresh token is supplied once used) and are blacklisted after rotation, minising XSS vulnerabilities.

<ins>Permissions and Customised Views</ins>

To demonstrate user permissions, you can change your access level in the profile page by selecting the is staff check input and the relevant role. Possible users are:

1. `MANAGER` - has read and write access to everything.
2. `CHEF` - has read and write access to inventory, menu pages.
3. `SALES` - has read and write access to orders and dashboard pages.
4. `IS STAFF` - has the same permissions as an anonymous user if not role is set.
5. `ANONYMOUS USER` - use is not logged in. Has read permissions on the menu page.

### Pages

A key aspect of this project is providing an interactive platform for small cafe owners to easily retrieve summary metrics of their business. The following describes the purpose and features of each page.

#### Login, Logout, Register

These pages are as described. When registering, you can select whether your user will by default be a staff member. This can easily be changed on the profile page when logged in.

#### Inventory

The inventory page is where you can add ingredients you have obtained and monitor which items are out of stock or low in stock. You can set the threshold of each ingredient to determine when a certain ingredient is considered low in stock.

#### Menu

The menu page is where you can add your menu items for your cafe. The ingredients you can use in your menu must be added as an inventory item first, even if you have none in stock.

#### Orders and Orders Archive

The orders page is where you can take customers' orders and visually view the status of each order. You can only add available menu items to the order. Orders that are completed are automatically moved to the orders archive page. The timestamps of each stage of the order (prepared, delivered) can be added to the data table under columns.

#### Dashboard

The dashboard is where you can gain an insight of your cafe business, including revenue, profits, inventory items that are low in stock or out of stock and menu items that are out of stock.


### Updates

1. Threshold field has been added to Inventory model.

---
## **Run locally with Docker**

### Prerequisites
- .env
- python3 migrate
- docker installation
- .Dockerfiles
- docker-compose.yml

### Setting up the backend

Here is a template of a `docker-compose.yml`` file that can be used.

```yml
version: '1'

services:
  # Create frontend container
  frontend: # Name of our service
    image: moonlight-cafe-frontend # name of image
    build: ./frontend # path to frontend dockerfile
    ports: # Port binding to host from docker container
      - "3000:3000" # Bind port 3000 of host to 3000 of container
    container_name: frontend-docker
    restart: always # What to do if container crashes
    links:
      - backend

  # Create backend container
  backend:
    image: moonlight-cafe-backend
    # Create backend container  
    build: ./backend
    ports:
      - "8000:8000"
    container_name: backend-docker
    restart: always
    links:
      - db

  # Create database container
  db:
    image: mysql:8
    env_file:
      - .env # path to .env file providing environmental variables for this mysql database
    ports:
      - "3307:3306"
    container_name: database-docker
    restart: always
    volumes:
      - db-data:/usr/src/

volumes:
  db-data:

```

Your .env file should contain the following variables.

```.env
MYSQL_HOST=*
MYSQL_PORT=*
MYSQL_DATABASE=*
MYSQL_ROOT_PASSWORD=*
```


---

### Feedback

If you experience any issues with this project, please open an issue.