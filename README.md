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

### Connecting Securely to Spider Sockey

When using this bot in tandem with a Spider Sockey websocket server, you will need to establish a secure connection via
the `wss` protocol. If your Spider Sockey server is using self-signed certificates, you will need to add the certificate
as a trusted certificate with blub. To do this, add the certificate to the `resources/auth/` directory while the container 
is running. The certificate should be named `server.crt`. To do this while the container is running, run the following 
command:
```sh
docker cp /path/to/server.crt <container_id_or_name>:/blub/resources/auth/server.crt
```
The reason this isn't copied over from the dockerfile is to avoid publishing the sensative certificate to the docker image.