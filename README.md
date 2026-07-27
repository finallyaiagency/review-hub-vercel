# FDE Review Hub

Source-controlled production dashboard for the Forward Design Engineer course.

## Deployment

Every push to `main` triggers `.github/workflows/deploy-vercel.yml`, which publishes this static dashboard to the existing Vercel project.

The workflow requires a repository secret named `VERCEL_TOKEN`. Project linkage is stored in `.vercel/project.json`; it contains project metadata, not credentials.

## Source of truth

- Learner journal: `/home/jarvis/.hermes/journal/course_journal.sqlite3`
- Dashboard source: `index.html`
- Production: https://review-hub-vercel.vercel.app

The journal updater should modify `index.html`, commit, and push. Do not edit journal data manually in the deployed page.