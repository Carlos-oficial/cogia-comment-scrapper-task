Core Task Summary:

- Given a file that contains a list of multiple Social network posts, you have to identify the Social Network from the link and retrieve the root post and all of its comments from the web (If its a video retrieve description if present otherwise just use title and date).

- For each link you should store the comments in a csv file or json file.

- You can declare a folder inside your project that process the file once dropped in, or pass the file path as an argument this is up to you.


Bonus:
 
 - Create an API with basic functionality to add a new link to crawl the results from and to retrieve the total ammount of comments <br>
   
       EXAMPLE:
       - POST url: "url": Creates the task to crawl for this url
       - GET url: Returns total ammount of comments for that Social Media Post
       - GET comments/url: returns all the comments from that url if they are in database 
  
 - Containerize the whole app with Docker


Requirements: <br>
- Final file must be generated and saved. You can also send the file to us with the link to the github project.