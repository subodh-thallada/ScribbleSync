# SribbleSync - UofTHacks XI Winner 
**Best use of AI in Application** 

Devpost: https://devpost.com/software/scribblesync

## Inspiration 🌟
Nostalgia comes through small items that trigger our sweet old memories. It reminds us of simpler times when a sticky note was all we needed to remember something important and have fun. Those satisfying moments of peeling the last layer of the memo pad, the embarrassing history of putting online passwords around the computer, and the hilarious actions of putting a thousand window XP sticky notes on the home screen are tiny but significant memories. In today's digital age, we wanted to bring back that simplicity and tangible feeling of jotting down notes on a memo sticker, but with a twist. ScribbleSync is our homage to the past, reimagined with today's technology to enhance and organize our daily lives.

## What it does 📝
ScribbleSync takes the traditional office memo sticker into the digital era. It's an online interface where you can effortlessly scribble notes, ideas, or events. These digital sticky notes are then intelligently synced with your Google Calendar with Large Language Models and Computer Vision, turning your random notes into scheduled commitments and reminders, ensuring that the essence of the physical memo lives on in a more productive and organized digital format.

## How we built it 🛠️
We built ScribbleSync using a combination of modern web technologies and APIs. The front-end interface was designed with HTML/CSS/JS for simplistic beauty. For the backend, we used Flask mainly and integrated Google Calendar API to sync the notes with the user’s calendar. We use state-of-the-art models from Google Vision, Transformer models from Hugginface for image analysis and fine-tuned Cohere models with our custom dataset in a semi-supervised manner to achieve textual classification of tasks and time relation.

## Challenges we ran into 😓
One of our biggest challenges was mainly incorporating multiple ML models and making them communicate with the front end and back end. Meanwhile, all of us are very new to hackathons so we are still adapting to the high-intensity coding and eventful environment.

## Accomplishments that we're proud of 🏆
We're incredibly proud of developing a fully functional prototype within the limited timeframe. We managed to create an intuitive, cute UI and the real-time sync feature works and communicates flawlessly. Overcoming the technical challenges and seeing our idea come to life has been immensely rewarding.

What we learned 📚
Throughout this journey, we've learned a great deal about API integration, real-time data handling, and creating user-centric designs. We also gained valuable insights into teamwork and problem-solving under pressure. Individually, we tried tech stacks that were unfamiliar to most of us such as Cohere and Google APIs, it is a long but fruitful process and we are now confident to explore other APIs provided by different companies.

## What's next for ScribbleSync 🚀
Our next step is to add practical and convenient functions such as allowing the sticky notes to set up drafts for email, schedules in Microsoft Teams and create Zoom links. We could also add features such as sticking to the home screen to enjoy those fun features from sticky notes in the good old days.