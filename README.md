INVENTORY MANAGEMENT SITE:

- **General:** This site was custom made and tailored for a client, if you wish to use this for another location please reach out to the owner Azamora96. 
- This is a simple inventory management website where there is one user, and they share a login, and they are able to add, edit, view, and delete items in their inventory.

- **Running the Site:** Download repo -> open Mountaineer-Marketplace-Inventory folder in your IDE of choice -> open flask_app.py -> Click Run -> visit your local host link to access page.

- **Login:** Reach Out to Owner for Login Information - **OR** -  If developer, create your own login in the Users table in the DB.
  
- **Adding a Product:** Click Add in the NAV bar -> All fields required except for image -> EXP Date field auto populated once Best By and Past Best By chosen -> Click Add Product.
  
- **Removing a Product:** Click Delete button in the row of Item to delete - **OR** - Press decrement(-) button until it hits zero, hit confirm for popup.
  
- **Editing a Product:** Click Edit button in the row of Item to edit -> Update desired fields and click Save Changes button.

- **Filtering the table:** Click an option in the Filter dropdown, table should be updated in ASC or DESC order based on choice.

- **Searching the table:** Search for the product you're looking for by clicking into the search bar and typing, the table should be updated as you type.

- **Exporting the table as CSV:** Click Export to CSV button -> Choose location to save .CSV file -> Choose name to save .CSV file as -> Click save.

- **Logging Out:** To Logout click the Logout button in the top left corner in the nav bar -> Should be brought back to login page.

- **Forgot Username/Password:** Click Forgot Password Button -> Admin will receive email with credentials. - There is a section in the helpers.py code for sending user information to the admin email.

- **Incorrect Credentials:** If you enter incorrect credentials at the login, it should give you a flash message indicating they were incorrect.

- **Correct Credentials:** If you enter correct crednetials at the login, you should be redirected to the home page where a table and other features are available. 
