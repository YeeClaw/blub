<img src="resources/readme/blub.png" alt="BlubBot logo" width="200"/>

Blub
----------------
### About
Blub is a simple discord but that I created to manage various discord tasks amongst me and my friends.
Here are some core features:
- Rich integration with minecraft servers and a slew of utility commands
- A websocket client used to interface with the SpiderSockey server to manage in game events and triggers
- "Activities" which are essentially mini-games that can be played in the discord server. A high score is
kept and stored in a postgres database and can be displayed at any time.

### Using Docker
Docker is the recommended way to run this bot and other means aren't officially supported. To run the bot,
you will need copy the `.env.template` file to the root of the project and rename it to `.env`. Additionally,
you will need to fill in the values for the environment variables in the `.env` file. 
Once you have done this, it's as simple as running the following command:
```shell
docker-compose up
```
A `-d` flag can optionally be added to run the container in detached mode.

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

### Postgres Database Structure
- database: postgres
  - schema: blub
    - table: activity
      - columns: activity_id*, activity_name
    - table: user
      - columns: user_id*, discord_id
    - table: highscore
      - columns: highscore_id*, user_id, activity_id, score

### Environment
- Python 3.12
  - discord.py
  - websockets
  - asyncio
  - psycopg2
- Docker
  - docker-compose
  - docker
- PostgreSQL

### Useful information
- [Discord.py Documentation](https://discordpy.readthedocs.io/en/stable/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### In the future
- Add more activities
- Add more utility commands
- Enfore DRY principles
- Expand the websocket client to support more features
- Expand postgres database

### Demos
- [Activity Demo](https://youtu.be/8k7e_wYJneI)
