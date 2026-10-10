# LNL — Professional Portfolio

**Production-style static portfolio for Lawal Nasir Lawal**.

The site has a persistent light/dark switch, responsive pages, case-study views, a live project filter, carefully labelled research records, and three independent printable CV formats. No Docker, credentials, Node, npm, API, or database is required.

## Fastest way to view it (Windows)

1. Extract this folder from the ZIP.
2. Double-click `START_PORTFOLIO.bat` (requires Python installed).
3. Open **http://localhost:4173** if the browser does not open automatically.
4. Keep the terminal open during preview; press `Ctrl+C` to stop.

Or open a terminal in this folder and run:

```powershell
py -m http.server 4173
```

**Do not double-click `index.html` directly.** Browser file-security rules block loading JSON from `file://`.

## Site map

- `/` — introduction, featured projects, current research, background, contact.
- `/work/` — all projects, filters.
- `/work/project/?id=fraudlens` — project case study (generated dynamically from the data, no route to edit).
- `/research/` — manuscripts and publications, with precise status labels.
- `/about/` — background, academic profile, skills, contact.
- `/cv/` — choose academic, professional, or research CV.
- `/cv/academic/`, `/cv/professional/`, `/cv/research/` — printable previews.

## Update content without changing website code

The entire public content lives in these files:

| Change | Edit |
| --- | --- |
| Headline, name, email/social links, skills | `content/profile.json` |
| Add / reorder / hide projects | `content/projects.json` |
| Add / update manuscripts and publications | `content/publications.json` |
| Academic CV | `content/cv-academic.json` |
| Professional CV | `content/cv-professional.json` |
| Research CV | `content/cv-research.json` |

### Use Pages CMS for an editor (recommended)

1. Push this folder into a **new GitHub repository** (e.g. `lawal-portfolio`). Keep it public only if you are comfortable publishing the content.
2. Go to **https://app.pagescms.org**, sign in with GitHub, and approve access only to your portfolio repository if possible.
3. Choose your portfolio repository. The included `.pages.yml` supplies editors for **Profile**, **Projects**, **Publications**, and **all three CV versions**.
4. Click a collection, add or update fields, upload photos/PDFs using the media picker, and save. Pages CMS commits the content change to GitHub.
5. If linked to Vercel, changes deploy through your usual GitHub deployment workflow. The portfolio itself never needs Pages CMS credentials or a CMS backend.

Pages CMS documentation: https://pagescms.org/docs/quick-start/ and https://pagescms.org/docs/configuration/content/list/

**Drafts:** Set `published` to false to hide a project/publication until ready. Use genuine status labels, especially for papers.

**New project:** Add a new object to the Projects list, with a unique `slug`, at least `title`, `summary`, `category`, and `published: true`. Add a cover under `media/projects/` and set `image` to `/media/projects/YOUR_IMAGE`. Every project automatically gets a case-study URL: `/work/project/?id=YOUR_SLUG`.

**New publication:** Add its record to Publications, including current `status`, `title` and `summary`. Leave `url` / `doi` empty until a public record exists. Do not mark a manuscript as published before actual publication.

## Updating the CVs

The CV hub deliberately maintains **three separate CV data files**, since different audiences need distinct summaries and ordering. The public identity, contact information, **university name, and graduation year** come from `profile.json` (the last two automatically fill any empty CV education fields).

- Open the desired CV preview; select **Print / Save as PDF** to create a PDF through the browser print dialog.
- Optionally upload your final designer-formatted PDF into `media/cv/` and set the relevant CV's `pdf` value to `/media/cv/YOURFILE.pdf`; a **Download PDF** link will appear automatically.
- Each CV has its own ordered experience, projects, research, education, skills, and certificates. Empty sections are hidden.
- **Initial content is a DRAFT:** verify university name, dates, employment duties, referees, and final wording before sharing.

### Adding professional experience

For the chosen CV, add an entry under `experience` with `title`, `organization`, `date`, and `details`. The final HTML/print template updates automatically. Do not publish claims or results you have not verified.

## Light/dark mode

A header button switches the entire website between light and dark. It remembers preference using browser local storage, respects the system theme on first visit, and can be operated from keyboard or mobile. Printable CV pages always use a paper-friendly light version.

## Deploy on Vercel (no build command)

1. Push the portfolio repository to GitHub.
2. Import that repository at https://vercel.com/new.
3. Set Framework Preset to **Other** (static website). Set **Build Command** to empty / override to blank if offered; use the **repository root** as the output directory (or leave Vercel's default static output settings when they already serve the root).
4. Deploy. The site is entirely static and requires **no environment variables**.
5. Visit `/work/`, `/research/`, `/cv/academic/` and test switching themes.

**Important:** The site uses root-relative `/` links and assumes deployment at a domain root. Deployments under `username.github.io/repository-name/` need a configured base path, so Vercel or a custom root domain is preferred.

## Editorial and privacy checklist

- Add your verified official university name and graduation date to profile/CV files.
- Verify all public project repository and demo URLs (some project links deliberately remain blank).
- Only advertise a manuscript status that is actually true; this starter marks maternal health work **manuscript in preparation**.
- Replace conceptual SVG artwork with real app screenshots when you have polished, safe screenshots to share.
- Do not put private addresses, access tokens, database credentials, telephone numbers or personal documents in the public repo.
- Check the three CV formats with actual target scholarship/job requirements before sending them.

## Tech / code structure

- Plain semantic HTML + modern CSS custom properties + small vanilla JS modules.
- All content fetched from `content/*.json`; safe text escaping and link validation are built into the renderer.
- No dependencies or build tooling; small enough to audit and reliable to publish.
- `.pages.yml` contains the optional Git-based CMS configuration.
- `build_pages.py` is only needed if you change shared HTML shell templates. Editing portfolio content **never** requires it.

Designed with progressive enhancement in mind; dynamic content requires JavaScript and an HTTP server.
