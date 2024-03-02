# E-commerce Web App
E-commerce Web App using Python w/ Django and it's templates. Main languages and frameworks consist of Python, Django, HTML, CSS, and Bootstrap. Database is PostgreSQL.

# Setting Up
To get the web app running you first need to setup your .env file. Within your .env file you'll add in these variables. We can just use the default database of PostgreSQL for now. A total of 6 variables are needed.

## .env file
These are the 6 variables you'll need to add. The location of the .env file matters. Ensure you have the .env file at the project's top-level directory (where Dockerfile & docker-compose.yml are located).
* `DB_NAME="postgres"`
* `DB_USER="postgres"`
* `DB_PASSWORD="postgres"`
* `DB_HOST="database"`
* `DB_PORT="5432"`
* `POSTGRES_PASSWORD="postgres"`

## Docker & Docker-compose
Docker should handle all the CLI (releated to setup) so you don't have to. You just need to set up the one .env file. Ensure you have docker and docker compose before starting. You can find more info below.<br><br>
[docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)<br>
[docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)<br>
[docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

# Running
Now that your .env file is set up. Ensure you're in the project's top-level directory before starting. You can run the app with docker-compose. In your terminal type in `docker-compose build` and then `docker-compose up`. Both these commands may take some time.

Within your browser go to `0.0.0.0:8000`, or `127.0.0.1:8000`, or `localhost:8000`. You should see a login page.

## Web App running before database
Docker sometimes will attempt to start the app before the database is running. If that's the case (though rare), you can simply run the `docker-compose up` command again.

# Features
* Users account (able to login, signup, reset password, and delete account)
* For a sense of money interaction, I've implemented pricing and credits
* All products are neatly displayed using CSS grid layout showing a brief overview of the product
  * Each product's image is clickable to view even more details about the product; this includes...
    * The list date
    * Universal Product Code (UPC) and or International Article Number (EAN)
    * Seller's profile picture (if they have one)
    * Seller's storefront link
    * Number of times the product page has been viewed
* Ability to list (either manually or through a UPC/EAN lookup), edit, and delete products
* Ability to filter by (all products, product's category, and product's condition)
* Ability to sort by products's (title, date, and views)
* Ability to search for products
  * Also contains an advanced search function
* Implemented pagination or paging to help separate content and for better presentation
* Has cart functionality with ability to remove items from the cart along with a check out function
* Some error checking includes, but is not limited to, ...
  * You must have enough credits on the account to satisfy the total price of all items in your cart in order to check out
  * Product can only be added to cart if you are the one that didn't list the product and if the product is not sold out or inactive
  * Product can only be edited and deleted if it's not sold out or and you are the one who listed it
  * If the product in cart is sold out, before you check out, a message will be displayed and the product will now be marked with a "SOLD OUT"
    * These "SOLD OUT" products cannot be purchased and you can only remove them from your cart
  * If the product in cart is inactive, before you check out, a message will be displayed and the product will now be marked with a "INACTIVE"
    * These "INACTIVE" products cannot be purchased and you can only remove them from your cart
  * Universal Product Code (UPC) and International Article Number (EAN) validation are done through Django forms
  * In matter of fact, all forms submitted to the back-end have some sort of validation done on them
  * To help prevent brute force, some views in Django will only accept UUIDs
    * If exposed, the UUID is shown to the user and not the ID/PK
* Dynamic messages with the help of Django messages and Bootstrap Modal
* Profile page with 5 different options to choose from
  * Settings where you can change your username/password/state or territory, upload profile/banner picture, and delete account
  * Wish List (to be implemented)
  * Listing History where you can view all the products that you have listed (active, inactive, and sold out)
  * Purchase History where you can view all the products that you have purchased
  * Login History (to be implemented though I may remove or replace it)
* Each user has their own storefront page which includes...
  * All the seller's products that are not sold out or inactive
  * Seller's profile picture and banner picture displayed at the top (if they have one)
  * Seller's basic information including username, which state/territory, and number of items sold
  * Users (but not the seller) can leave a feedback on the seller's storefront
    * Accurate Description (1-5)
    * Shipping Speed (1-5)
    * Shipping Cost (1-5)
    * Communication (1-5)
  * Users can also view the feedback left by other users or themselves
    * The user who left the feedback
    * The date of the feedback
    * The overall rating is turned into a picture (emoji smile for good, emoji neutral for neutral, and emoji frown for bad)
    * Accurate Description (1-5)
    * Shipping Speed (1-5)
    * Shipping Cost (1-5)
    * Communication (1-5)
    * The comment