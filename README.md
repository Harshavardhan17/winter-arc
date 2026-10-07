# Winter Arc

A tiny installable web app (PWA) for a shared Winter Arc challenge: one common daily checklist,
everyone ticks their own boxes, and a colourful leaderboard (points, streaks, perfect days,
calendar heatmap, confetti on a 100% day). Works on iPhone and Android, syncs live between phones.

No build step. Files: `index.html`, `manifest.webmanifest`, `sw.js`, `icons/`.

## One-time setup (about 10 minutes, only the organiser does this)

### 1. Free shared database (Firebase Realtime Database, no card needed)

1. Open https://console.firebase.google.com with your personal Google account.
2. **Create a project** -> any name (e.g. `winter-arc`) -> Google Analytics can be turned off -> Create.
3. Left menu **Build -> Realtime Database -> Create database** -> pick a location -> **Start in locked mode** -> Enable.
4. Open the **Rules** tab, replace everything with the contents of `database.rules.json`, click **Publish**.
5. Copy the database URL shown at the top of the **Data** tab,
   e.g. `https://winter-arc-1234-default-rtdb.asia-southeast1.firebasedatabase.app`.

### 2. Free hosting (GitHub Pages, from your personal GitHub account)

1. On github.com create a new repository, e.g. `winter-arc` (Public is required for free Pages).
2. Push this folder (use your personal identity, set locally for this repo only):

       cd ~/winter-arc
       git config user.name  "<your personal name>"
       git config user.email "<your personal email>"
       git add -A && git commit -m "Winter Arc app"
       git branch -M main
       git remote add origin https://github.com/<your-username>/winter-arc.git
       git push -u origin main

3. Repo **Settings -> Pages -> Build and deployment -> Deploy from a branch -> main / (root) -> Save**.
4. After ~1 minute the app is live at `https://<your-username>.github.io/winter-arc/`.

(Any static host works: Netlify / Vercel / Cloudflare Pages drag-and-drop of this folder too.)

### 3. Create the challenge

1. Open the app URL on your phone -> paste the database URL into **Start a new shared challenge** -> Create.
2. Set name / start date / length (defaults to today -> Dec 31), then create your player.
3. **Setup -> Invite -> Share link** and send it to your friend (WhatsApp etc).

## Joining (friend, no signup)

- Open the invite link -> type your name, pick an animal + colour -> Join.
- **iPhone:** open the link in **Safari** -> Share button -> **Add to Home Screen** -> Add.
- **Android:** open in **Chrome** -> menu (three dots) -> **Add to Home screen / Install app**.
- Add to the home screen *after* joining, so the icon opens straight into your own list.
  If a home-screen icon ever opens the welcome page, paste the invite link into "Got an invite link?".

## How the scoring works

- Each checklist item has points (default 10). A 100% day adds a 20-point bonus.
- A streak day needs at least the configured % done (default 80%). Today never breaks a streak
  while it is still in progress.
- Adding an item mid-challenge counts from today; removing one keeps past days intact.
- You can tap past days in the Calendar to fix a missed tick.
- Optional (bonus) habits add their points when ticked but never count toward the daily %,
  perfect day or streak. Add one any time with "+ optional habit" on the Today screen.
- Tap any habit on the Today screen to rename it, change points, flip required/optional or remove it.
  Edits apply from today forward; past days keep the version they had, so history, streaks and the
  leaderboard are never rewritten.

## Privacy note

There are no accounts: anyone who has the invite link can open and edit that challenge, so only
share it with your crew. The room id in the link is a random 12-character code. The Firebase URL
is a public web endpoint, not a secret.

## Local testing

    python3 dev/mock_firebase.py 8788 &      # in-memory stand-in for the Firebase REST API
    python3 -m http.server 8787              # then open http://127.0.0.1:8787 and use http://127.0.0.1:8788 as the database URL

Or click "Just try it on this device" for a no-database demo.
