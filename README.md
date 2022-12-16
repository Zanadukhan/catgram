# catgram
A script for mass uploading pics to instagram from google drive.
I had the idea to create this script for myself when I got a new kitten and a friend recommended that I create an instagram for him.
Hence all the refrences to cat in this but it can be adjusted for any purpose.

# What does this do?
1. This script looks into your google drive and pulls out images from a folder that matches the correct conditions 
  - You are given an option to create a new folder when you run the script
2. The pictures are downloaded and moved into the 'instagram_uploads' folder so that the instabot knows where to search for JPGs


# How to use
1. Follow the instructions under "authorize credentials for a desktop application" and move the json (rename to credentials.json) to the google_auth folder
2. Replace all the placeholders i.e instagram username and password
3. Running the program opens the google api where it asks you to authorize to edit, view etc, say yes and close the window
4. Your google drive is checked for a "cat pics" folder, if you don't have one, it'll create a new one and prompt you to rerun the script.

# Issues
1. Instagram uploading is handled by a library called 'instabot'. While uploading pictures works fine, the upload video function is broken and doesn't work.
2. From what I've read, google drive api doesn't actually download the jpg directly but converts it to a bitmap or something. 
   Regardless, it can result in downloaded images being rotated 90 degrees.

# Planned Feature
1. Giving the user the option of being presented each photo and assigning a caption to be posted with it.