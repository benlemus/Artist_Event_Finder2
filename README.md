# WHERE'S MY ARTIST

### Link To Website

https://artist-event-finder2.onrender.com/

### Overview

This is a web application that connects to a users Spotify account to automatically search for any upcoming events pertaining to their most listened to artists.
A user can easily link to buy tickets, see events near them they might like, see where their favorite artists are performing and see currently trending events.

### Login Page
<img width="1899" height="906" alt="landing-page" src="https://github.com/user-attachments/assets/0ba6b3f7-ffe0-4f0e-b107-f03ac005fe4b" />

### Pre Spotify Connection
<img width="1902" height="907" alt="pre-spotify-login" src="https://github.com/user-attachments/assets/77ce5054-2813-4a5b-9e1d-8f820d8e2966" />

### Post Spotify Connection
<img width="1899" height="906" alt="post-spotify-login" src="https://github.com/user-attachments/assets/8d0bbaa1-7cce-4950-9037-ae1e5292bc59" />

### See Top Artist Events
<img width="1896" height="673" alt="top-artist-events" src="https://github.com/user-attachments/assets/52c1f18b-449e-4e36-9536-313a359f6f09" />

### See Top Played Tracks
<img width="1885" height="542" alt="top-tracks" src="https://github.com/user-attachments/assets/fd70573b-86d6-4e09-bc37-d54dcc3d42d7" />

## Stack

    - Python
    - Javascript
    - WTForms
    - Bcrypt
    - SQL

## Deployment

    - SupaBase
    - Render

## Features

    - See up to date events for users favorite artists
    - See where your favorite artists are performing
    - See your top artists on Spotify
    - See your top tracks
    - Find other events near you
    - See trending events
    - Easily linked to purchase tickets

## Getting Around the Application

    Getting around here is pretty easy. At the homepage, if you are not already logged in, you will be prompted to do so or create an account. You can also see some trending events.
    Once logged in you will not be able to see your top artists/events/tracks yet! You need to connect your Spotify account by simply clicking on the connect spotify in the navbar and follow the prompts.
    After you have connected your Spotify account you have full access to the application.
    You can now see your personalized home page to view your favorite artists, favorite artists events and top tracks.
    Where ever you see an event you can add to your wishlist or click the link to get tickets.
    In the navbar, there are links to see your wishlist, go to your account or logout.
    Your wishlist that shows all your events you will one day go to!
    At any time you are allowed to change your profile details in the My Account section and under the edit details. You can also change your password here.

## APIS Used

    - Ticketmaster API
    - Spotify API

## Testing

    There are two testing files. One to test all of the models connecting directly to the database and one to test all of the flask routes. To use them, simply clone the repo, make sure you have all the requirements and run: python -m unittest [full_file_name]
