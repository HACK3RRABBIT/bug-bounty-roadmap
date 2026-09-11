# Deploying to Cloudflare

This app is a static export (`next.config.ts` sets `output: "export"`) — plain HTML/CSS/JS,
deployable via Wrangler once the API token has the right permission.

## Build

```bash
cd web
npm install
npm run build      # writes static site to web/out
```

## Deploy (once the token works — see below)

Modern path (Workers + Static Assets, `wrangler.jsonc` already configured):

```bash
CLOUDFLARE_API_TOKEN=<token> CLOUDFLARE_ACCOUNT_ID=<account-id> npx wrangler deploy
```

Classic path (Cloudflare Pages) also works if you'd rather use Pages:

```bash
CLOUDFLARE_API_TOKEN=<token> CLOUDFLARE_ACCOUNT_ID=<account-id> \
  npx wrangler pages project create bug-bounty-roadmap --production-branch main --force
CLOUDFLARE_API_TOKEN=<token> CLOUDFLARE_ACCOUNT_ID=<account-id> \
  npx wrangler pages deploy out --project-name=bug-bounty-roadmap
```

## The token permission that was missing

The token tried during this session (`cfat_...` created 2026-09-11) could read account/Pages/Workers
data but **could not write** — both `wrangler deploy` (Workers) and `wrangler pages project create`
(Pages) failed identically with `Authentication error [code: 10000]`.

To fix, create a new token at **dash.cloudflare.com → My Profile → API Tokens → Create Token** with:

- **Workers Scripts: Edit** (for the `wrangler deploy` / Workers Static Assets path), or
- **Cloudflare Pages: Edit** (for the classic Pages path)

— either the ready-made "Edit Cloudflare Workers" template, or a custom token with that permission
added to the account scope. Never commit the token to this repo; pass it as an environment variable
to the deploy command only.

## Analytics

Once deployed, Cloudflare gives you analytics with **no extra setup**:
- **Workers/Pages built-in analytics** (requests, bandwidth) appears automatically in the dashboard
  for the deployed project — nothing to configure.
- **Cloudflare Web Analytics** (privacy-first, cookieless real-user monitoring) can additionally be
  enabled from **dash.cloudflare.com → Analytics & Logs → Web Analytics → Add a site**, which gives
  you a small beacon `<script>` snippet to drop into `src/app/layout.tsx`.
