# Project Testing

[Wild Swimming link to the website](https://flask-wild-swimming-1dc7d2b9c0b6.herokuapp.com/home) 

## Manual Testing

Manual testing is crucial in software development, providing unique advantages that automated testing cannot. Human testers bring intuition, creativity, and adaptability, identifying user experience issues that may go unnoticed. Manual testing is particularly useful in exploratory testing and UI/UX evaluation. Combining manual and automated testing leads to high-quality products. 
Manual testing has been undertaken for the wild swimming website. Below is the summary of the steps and results.

### Home page
<br>

| Test Case | Description                                     | Steps                                                  | Expected Result                                            | Pass/Fail | Comment                                               |
|-----------|-------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------------|-----------|-------------------------------------------------------|
| Navigation| Check if navigation links are working           | 1. Click on "Home" link                               | Landing on the homepage                                   | Pass      |                                                       |
|           |                                                 | 2. Click on "Blog" link                               | Redirected to the blog page                                | Pass      |                                                       |
|           |                                                 | 3. Click on "Login" link                              | Redirected to the login page                               | Pass      |                                                       |
|           |                                                 | 4. Click on "Register" link                           | Redirected to the register page                            | Pass      |                                                       |
| Homepage  | Check the content and layout of the homepage    | 1. Verify the presence of the welcome message         | "Welcome to the hub for outdoor swimmers" is displayed    | Pass      |                                                       |
|           |                                                 | 2. Verify the "Read Blog" button                      | Button is present and clickable                           | Pass      |                                                       |
| Flash Messages | Check if flash messages are displayed      | - No specific steps, just observe the flash messages   | Flash messages (if any) are displayed                      | Pass      | No messages displayed as expected                                                       |
| Footer    | Check the content and layout of the footer      | - No specific steps, just observe the footer           | Footer contains the helper message                         | Pass      |                                                       |
| Responsive| Check if the page is responsive                 | - Resize the browser window                           | Page content adjusts appropriately for different screen sizes | Pass  |                                                       |
| Accessibility| Check if the page is accessible               | - Use a screen reader     | No accessibility issues are reported                        | Pass  |                                                       |

### Blog page - user not logged in
<br>

| Test Case | Description                                     | Steps                                                  | Expected Result                                            | Pass/Fail | Comment                                               |
|-----------|-------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------------|-----------|-------------------------------------------------------|
| Navigation| Check if navigation links are working           | 1. Click on "Home" link                               | Landing on the homepage                                   | Pass      |                                                       |
|           |                                                 | 2. Click on "Blog" link                               | Stay on the blog page                                     | Pass      |                                                       |
|           |                                                 | 3. Click on "Login" link                            | Redirected to the login page                            | Pass      |                                                       |
|           |                                                 | 4. Click on "Register" link                        | Redirected to the register page                        | Pass      |                                                       |
| Homepage  | Check the content and layout of the homepage    | - No specific steps, observe the layout and content   | Content is displayed properly, no visual issues           | Pass      |                                                       |
| Flash Messages | Check if flash messages are displayed      | - No specific steps, just observe the flash messages   | Flash messages (if any) are displayed                      | Pass      | Message prompt to login displayed when clicked on "Write Post" button                                                       |
| Blog Posts | Check if blog posts are displayed correctly   | - Verify the content of each blog post                 | Blog posts are displayed with correct information         | Pass      |                                                       |
| Search Functionality | Check if the search functionality works  | 1. Enter a valid search query in the search bar        | Relevant blog posts are displayed based on the search query | Pass  |                                                       |
|           |                                                 | 2. Click on "Reset" button                            | Reset the search and show all blog posts                  | Pass      |                                                       |
| Responsive| Check if the page is responsive                 | - Resize the browser window                           | Page content adjusts appropriately for different screen sizes | Pass  |                                                       |
| Accessibility| Check if the page is accessible               | - Use a screen reader  | No accessibility issues are reported                        | Pass  |                                                       |


### Blog page - user logged in
<br>

| Test Case | Description                                     | Steps                                                  | Expected Result                                            | Pass/Fail | Comment                                               |
|-----------|-------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------------|-----------|-------------------------------------------------------|
| Navigation| Check if navigation links are working           | 1. Click on "Home" link                               | Landing on the homepage                                   | Pass      |                                                       |
|           |                                                 | 2. Click on "Blog" link                               | Stay on the blog page                                     | Pass      |                                                       |
|           |                                                 | 3. Click on "Profile" link                            | Redirected to the profile page                            | Pass      |                                                       |
|           |                                                 | 4. Click on "Create Post" link                        | Redirected to the create post page                        | Pass      |                                                       |
|           |                                                 | 5. Click on "Logout" link                             | Perform logout and redirect to the homepage              | Pass      |                                                       |
| Homepage  | Check the content and layout of the homepage    | - No specific steps, observe the layout and content   | Content is displayed properly, no visual issues           | Pass      |                                                       |
| Flash Messages | Check if flash messages are displayed      | - No specific steps, just observe the flash messages   | Flash messages (if any) are displayed                      | Pass      | No messages displayed as expected                                                      |
| Blog Posts | Check if blog posts are displayed correctly   | - Verify the content of each blog post                 | Blog posts are displayed with correct information         | Pass      |                                                       |
| Search Functionality | Check if the search functionality works  | 1. Enter a valid search query in the search bar        | Relevant blog posts are displayed based on the search query | Pass  |                                                       |
|           |                                                 | 2. Click on "Reset" button                            | Reset the search and show all blog posts                  | Pass      |                                                       |
| Post Actions | Check if edit and delete actions work       | 1. Click on "Edit" for a post                         | Redirected to the edit post page                           | Pass      |                                                       |
|           |                                                 | 2. Click on "Delete" for a post                       | Modal appears asking for confirmation to delete the post  | Pass      |                                                       |
|           |                                                 | 3. Confirm deletion in the modal                     | Post is deleted, and user is redirected to blog page      | Pass      |                                                       |
| Responsive| Check if the page is responsive                 | - Resize the browser window                           | Page content adjusts appropriately for different screen sizes | Pass  |                                                       |
| Accessibility| Check if the page is accessible               | - Use a screen reader  | No accessibility issues are reported                        | Pass  |                                                       |


### Profile page
<br>

| Test Case | Description                                        | Steps                                                               | Expected Result                                               | Pass/Fail | Comment                                                |
|-----------|----------------------------------------------------|---------------------------------------------------------------------|--------------------------------------------------------------|-----------|--------------------------------------------------------|
| Navigation| Check if navigation links are working              | 1. Click on "Home" link                                            | Landing on the homepage                                      | Pass      |                                                        |
|           |                                                    | 2. Click on "Profile" link                                         | Stay on the profile page                                     | Pass      |                                                        |
|           |                                                    | 3. Click on "Delete" button inside the modal for a post            | Confirm deletion and redirect to blog page                  | Pass      |                                                        |
|           |                                                    | 4. Click on "Edit" button inside the modal for a post              | Redirect to the edit profile page                            | Pass      |                                                        |
| Profile   | Check if the user's profile information is displayed| - Observe the content in the "Hello and welcome Al!" and "Your posts:" sections | User's name and post information are displayed correctly   | Pass      |                                                        |
| Blog Posts| Check if user's blog posts are displayed correctly | - Verify the content of each user's blog post                      | User's blog posts are displayed with correct information    | Pass      |                                                        |
| Delete Post| Check if the delete post modal works              | 1. Click on "Delete" button for a post                             | Modal appears asking for confirmation to delete the post    | Pass      |                                                        |
|           |                                                    | 2. Confirm deletion in the modal                                   | Post is deleted, and user is redirected to the blog page    | Fail      | Post deleted but user was redirected to Blog Page                                                       |
|           |                                                    | 3. Cancel deletion in the modal                                   | User is redirected to the Profile page    | Fail      | User redirected to Blog Page                                                       |
| Edit Post | Check if the edit post functionality works        | 1. Click on "Edit" button for a post                               | Redirect to the edit profile page                            | Pass      |                                                        |
| Responsive| Check if the page is responsive                    | - Resize the browser window                                        | Page content adjusts appropriately for different screen sizes | Pass  |                                                        |
| Accessibility| Check if the page is accessible                  | - Use a screen reader              | No accessibility issues are reported                         | Pass      |                                                        |


### Create Post Page
<br>

| Test Case | Description                                        | Steps                                                               | Expected Result                                               | Pass/Fail | Comment                                                |
|-----------|----------------------------------------------------|---------------------------------------------------------------------|--------------------------------------------------------------|-----------|--------------------------------------------------------|
| Navigation| Check if navigation links are working              | 1. Click on "Home" link                                            | Landing on the homepage                                      | Pass      |                                                        |
|           |                                                    | 2. Click on "Blog" link                                           | Redirect to the blog page                                    | Pass      |                                                        |
|           |                                                    | 3. Click on "Profile" link                                        | Redirect to the profile page                                 | Pass      |                                                        |
|           |                                                    | 4. Click on "Logout" link                                         | Log out the user and redirect to the homepage               | Pass      |                                                        |
| Create Post| Check if the create post form works                | 1. Fill in the form with valid data                               | Form fields are populated with the entered data             | Pass      |                                                        |
|           |                                                    | 2. Submit the form                                                | Post is created, and user is redirected to the blog page    | Pass      |                                                        |
|           |                                                    | 3. Leave any required field blank and submit                    | Error message is displayed, and form is not submitted       | Pass      |                                                        |
|           |                                                    | 4. Enter data that exceeds maximum length and submit            | Error message is displayed, and form is not submitted       | Pass      |                                                        |
|           |                                                    | 5. Verify character limits for title, content, and keywords     | Limits are enforced, and appropriate messages are displayed  | Pass      |                                                        |
|           |                                                    | 6. Verify the presence of cancel and submit buttons             | Both buttons are visible and functional                     | Pass      |                                                        |
| Responsive| Check if the page is responsive                    | - Resize the browser window                                        | Page content adjusts appropriately for different screen sizes | Pass  |                                                        |
| Accessibility| Check if the page is accessible                  | - Use a screen reader              | No accessibility issues are reported                         | Pass      |                                                        |

### Edit Post Page
<br>

| Test Case | Description                                       | Steps                                                                | Expected Result                                                | Pass/Fail | Comment                                             |
|-----------|---------------------------------------------------|----------------------------------------------------------------------|---------------------------------------------------------------|-----------|-----------------------------------------------------|
| Edit Post | Check if the edit post form works                 | 1. Open the edit post page for an existing post                       | Form is populated with post data                               | Pass      |                                                     |
|           |                                                   | 2. Modify the title, content, and tags                               | Changes are reflected in the form fields                        | Pass      |                                                     |
|           |                                                   | 3. Submit the form                                                   | Post is updated, and user is redirected to the blog page       | Pass      |                                                     |
|           |                                                   | 4. Leave any required field blank and submit                       | Error message is displayed, and form is not submitted          | Pass      |                                                     |
|           |                                                   | 5. Enter data that exceeds maximum length and submit               | Error message is displayed, and form is not submitted          | Pass      |                                                     |
|           |                                                   | 6. Verify character limits for title, content, and keywords        | Limits are enforced, and appropriate messages are displayed     | Pass      |                                                     |
|           |                                                   | 7. Verify the presence of "Cancel editing" and "Update post" buttons | Both buttons are visible and functional                       | Pass      |                                                     |
| Responsive| Check if the page is responsive                   | - Resize the browser window                                          | Page content adjusts appropriately for different screen sizes | Pass      |                                                     |
| Accessibility| Check if the page is accessible                 | - Use a screen reader                | No accessibility issues are reported                          | Pass      |                                                     |

### Login Page
<br>

| Test Case | Description                        | Steps                                       | Expected Result                              | Pass/Fail | Comment                        |
|-----------|------------------------------------|---------------------------------------------|----------------------------------------------|-----------|--------------------------------|
| Log In    | Check if the login form works       | 1. Open the login page                      | Form is displayed with username and password fields | Pass      |                                |
|           |                                    | 2. Enter valid username and password      | User is redirected to the home or profile page (depending on the application) | Pass      |                                |
|           |                                    | 3. Leave either username or password blank and submit | Error message is displayed, and form is not submitted | Pass      |                                |
|           |                                    | 4. Enter an invalid username or password and submit | Error message is displayed, and form is not submitted | Pass      |                                |
| Responsive| Check if the page is responsive    | - Resize the browser window                 | Page content adjusts appropriately for different screen sizes | Pass      |                                |
| Accessibility| Check if the page is accessible  | - Use a screen reader | No accessibility issues are reported       | Pass      |                                |
| Registration| Check if the "Create Account" link works | 1. Click on the "Create Account" link   | User is redirected to the registration page | Pass      |                                |
|           |                                    | 2. Verify the presence of the registration form | Registration form is displayed               | Pass      |                                |

### Registration Page
<br>

| Test Case | Description                        | Steps                                       | Expected Result                              | Pass/Fail | Comment                        |
|-----------|------------------------------------|---------------------------------------------|----------------------------------------------|-----------|--------------------------------|
| Register  | Check if the registration form works | 1. Open the registration page              | Form is displayed with username and password fields | Pass      |                                |
|           |                                    | 2. Enter valid username and password      | User gets registred and is redirected to the login page | Pass      |                                |
|           |                                    | 3. Leave either username or password blank and submit | Error message is displayed, and form is not submitted | Pass      |                                |
|           |                                    | 4. Enter an invalid username or password and submit | Error message is displayed, and form is not submitted | Pass      |                                |
|           |                                    | 5. Enter existing username and submit | Error message is displayed, and form is not submitted | Pass      | A flash message is displayed, prompting the user to choose another username.                                 |
| Responsive| Check if the page is responsive    | - Resize the browser window                 | Page content adjusts appropriately for different screen sizes | Pass      |                                |
| Accessibility| Check if the page is accessible  | - Use a screen reader | No accessibility issues are reported       | Pass      |                                |
| Log In Link| Check if the "Log In" link works   | 1. Click on the "Log In" link               | User is redirected to the login page        | Pass      |                                |
|           |                                    | 2. Verify the presence of the login form    | Login form is displayed                      | Pass      |                                |



## Validation checks
### W3C HTML
[W3C HTML Validator](https://validator.w3.org/nu/) has been used to test HTML. The website has no errors. 
<br>

![Link to the screenshots file](static/images/w3c-html-1.png)
![Link to the screenshots file](static/images/w3c-html-2.png)
![Link to the screenshots file](static/images/w3c-html-3.png)
![Link to the screenshots file](static/images/w3c-html-4.png)

### CSS
[W3C CSS Validator](https://jigsaw.w3.org/css-validator/) has been used to test Cascading Style Sheets. The website has no errors. The file that has been checked is [script.js](/static/css/style.csss).
<br>

![Link to the screenshots file](static/images/w3c-css.png)

### Javascript Validation
[ JSHint](https://jshint.com/) has been used to test javascript. The website has no errors. The file that has been checked is [script.js](/static/js/script.js).
<br>

![Link to the screenshots file](static/images/jshint.png)

### Python Validation
[ CI Python linter](https://pep8ci.herokuapp.com/) has been used to the javascript. The website has no errors. The file that has been checked is [app.py](/app.py).
<br>

![Link to the screenshots file](static/images/ci_python_linter.png)
