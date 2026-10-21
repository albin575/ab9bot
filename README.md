### song-bot
```
You can download youtube to MP3 from telegram bot #musics
with & without commands
```

## Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/albin575/albinnewsongbot)

1. Click the **Deploy to Render** button above.
2. Connect your GitHub account and give the service a name.
3. Fill in the environment variables when asked:
   - `APP_ID` and `API_HASH` — from https://my.telegram.org
   - `BOT_TOKEN` — from @BotFather
   - `OWNER`, `START_MSG`, `START_IMG` — optional, defaults are fine
4. Click **Deploy**. The bot starts automatically after the build.

### "Sign in to confirm you're not a bot"

YouTube sometimes bot-checks cloud server IPs, which makes downloads fail.
If that happens, set **one** of these optional env vars and restart:

- `YOUTUBE_PO_TOKEN` — PoToken pairs in `client+token` form, comma-separated
  (e.g. `web+XXX,android+YYY`). Generate one with the `bgutil-ytdlp-pot-provider`
  script from a logged-in browser session.
- `YOUTUBE_COOKIES_FILE` — absolute path to a Netscape-format `cookies.txt`
  exported from a logged-in YouTube browser session.

> Free plan note: the service sleeps after 15 minutes without web traffic.
> Keep it awake with a free monitor (e.g. UptimeRobot) pinging `https://<your-app>.onrender.com/` every 5 minutes.

## Deploy - Simplest Way
##### Deploy - with /song command

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/albin575/song-bot/tree/main)

##### Deploy - Without Command
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/albin575/song-bot)

## Deploy Hard Way
No Any Hard Ways Deploy simple way 🤗🤣
