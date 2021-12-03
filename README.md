# Veloxxity-Sentiment-Analysis-Project
UT Dallas Senior Design Project, Sponsor: Veloxxity

The goal of this project in accordance with the
stakeholder (Sponsor: Veloxxity LLC) requirements is to develop a sustainable and interactive
sentiment analysis that collects viral posts with regards to the international conflicts in the South
China Sea. The application will be deployed as a Representational state transfer (REST) API with
the objective of providing a solution to the distribution of misinformation on online social media
platforms.

Running ytapiv2.py


  First we need credentials from google API.
  In order to get credentials, visit https://developers.google.com/youtube/v3/getting-started and download the AUTHpath in JSON format and rename the file as "credentials.json"     and save it to the same directory as ytapivs.py.
  We need util.py in the same directory as well.
  Everytime the token expired, revisit the google website to get refreshed token and update the credentials file.
  Once you get the new credentials, comment out line20-22 in util.py and authenticate yourself through google to run ytapiv2.py. After that you can uncomment the same lines until the token expired.
  
