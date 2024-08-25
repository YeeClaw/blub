<img src="resources/readme/blub.png" alt="BlubBot logo" width="200"/>

Blub
----------------
### About
Blub is a simple discord but that I created to manage various discord tasks amongst me and my friends.
Here are some core features:
- Rich integration with minecraft servers and a slew of utility commands
- A websocket client used to interface with the SpiderSockey server to manage in game events and triggers

### Using Docker
When using docker to run a "blub" instance for the first time, the program will throw an error. This is because a proper
`.env` file needs to be established in the root directory (`/blub`) of the bot. A template for the `.env` file can be
found under `./resources/environment/.env.template`. From `/blub`, run the following commands:
- Copy the template to the root directory under a new name (.env)
```sh
cp ./resources/environment/.env.template ./.env
```
- Edit (using nano!) the `.env` file to include the necessary environment variables (make sure you save changes :))
```sh
nano .env
```
And from there you should be good to go! You can either run `python src/main.py` from the docker shell or just restart 
the docker container.