# Deploy Frank to Azure — one command, three secrets, push

All you need: **this fork and an Azure account.** Nothing installs on your
laptop — the one setup command runs in Azure Cloud Shell (a terminal in
your browser), and GitHub Actions does everything else.

## 0. What you'll end up with

Push to `main` (touching `frank/**`) → GitHub Actions builds Frank from
source in Azure and deploys him to **Azure Container Apps** → the run
summary prints his HTTPS URL. Every client from the connect-everywhere lecture (4.7) connects to it.

## 1. Create the deploy credential (one Cloud Shell command)

1. Sign in at [portal.azure.com](https://portal.azure.com). Grab your
   **Subscription ID** (Portal → Subscriptions).
2. Open **Cloud Shell** ([shell.azure.com](https://shell.azure.com) —
   choose Bash). Run, substituting your subscription id:

```bash
az ad sp create-for-rbac \
  --name shipit-frank-deploy \
  --role contributor \
  --scopes /subscriptions/<YOUR_SUBSCRIPTION_ID> \
  --json-auth
```

3. Copy the entire JSON block it prints. That's your deploy credential.

> Least privilege note (Lecture 4.6): contributor-on-subscription is the
> friction-free classroom setting. At work, scope to one resource group
> and prefer OIDC federated credentials over a secret — same workflow,
> different login step.

## 2. Add three secrets to your fork

Fork → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Value |
|---|---|
| `AZURE_CREDENTIALS` | the JSON from step 1, pasted whole |
| `FRANK_AUTH_TOKEN` | any long random string — in Cloud Shell: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `FRANK_GITHUB_TOKEN` | a fine-grained PAT for **your fork only**, permission **Actions: read** (GitHub → Settings → Developer settings) |

## 3. Enable workflows on your fork

GitHub disables workflows on forks until you opt in: **Actions tab →
"I understand my workflows, go ahead and enable them."**

## 4. Push (or click)

Either push any change under `frank/`, or run the **Deploy Frank**
workflow manually (Actions → Deploy Frank → Run workflow). First run
takes a few minutes — it's creating the resource group, registry, and
Container Apps environment. Every run ends with:

> 🟢 **Frank is live** — MCP endpoint: `https://frank.<env>.azurecontainerapps.io/mcp`

## 5. Connect a client

```bash
claude mcp add --transport http frank https://<FQDN>/mcp \
  --header "Authorization: Bearer <your FRANK_AUTH_TOKEN>"
```

Then ask: *"Is the pipeline healthy?"* — and watch Frank answer from your
fork's Actions and his own container.

## Cost & teardown

Container Apps scales to zero and the monthly free grant comfortably
covers course use. When you're done:

```bash
az group delete --name shipit-rg --yes --no-wait
```

One command removes everything the workflow created.

## If something goes wrong

- **Login step fails** → `AZURE_CREDENTIALS` isn't the full JSON, or the
  service principal was scoped to a resource group that doesn't exist yet.
- **First deploy is slow** → normal; the source build + environment
  creation happens once.
- **Workflow doesn't trigger** → workflows not enabled on the fork
  (step 3), or your change didn't touch `frank/**`.
- **401 from Frank** → the `Authorization: Bearer` header doesn't match
  `FRANK_AUTH_TOKEN`.
- The `az` CLI evolves — if a flag is rejected, check
  `az containerapp up --help` in Cloud Shell.
