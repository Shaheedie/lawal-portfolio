"""Zero-dependency checks to help keep public content accurate and deployable."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
errors = []


def fail(message):
    errors.append(message)


def load(name, expected):
    file = CONTENT / f'{name}.json'
    try:
        value = json.loads(file.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        fail(f'{file.relative_to(ROOT)}: {exc}')
        return expected()
    if not isinstance(value, expected):
        fail(f'{file.relative_to(ROOT)} must contain a {expected.__name__}.')
        return expected()
    return value


def link_ok(url):
    if not url:
        return True
    if not isinstance(url, str):
        return False
    if url.startswith('/') and not url.startswith('//'):
        return (ROOT / url.lstrip('/')).is_file()
    parsed = urlparse(url)
    return parsed.scheme in {'https', 'http'} and bool(parsed.netloc)


profile = load('profile', dict)
for key in ('name', 'degree', 'gpa'):
    if not str(profile.get(key, '')).strip():
        fail(f'profile.json is missing {key}.')
for key in ('github', 'linkedin'):
    if not link_ok(profile.get(key, '')):
        fail(f'profile.json has an invalid {key} URL.')

projects = load('projects', list)
seen = set()
for i, p in enumerate(projects, 1):
    location = f'projects.json entry {i}'
    if not isinstance(p, dict):
        fail(f'{location} must be an object.')
        continue
    slug = p.get('slug', '')
    if not isinstance(slug, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        fail(f'{location}: slug must use lowercase letters, numbers and hyphens.')
    if slug in seen:
        fail(f'{location}: duplicate slug {slug!r}.')
    seen.add(slug)
    for key in ('title', 'summary', 'category'):
        if not str(p.get(key, '')).strip():
            fail(f'{location}: {key} is required.')
    for key in ('published', 'featured'):
        if key in p and not isinstance(p[key], bool):
            fail(f'{location}: {key} must be true or false.')
    for key in ('image', 'github', 'demo'):
        if not link_ok(p.get(key, '')):
            fail(f'{location}: {key} must be a valid public path or HTTP(S) URL.')

statuses = {'Research in progress', 'Manuscript in preparation', 'Submitted / under review', 'Preprint', 'Accepted', 'Published'}
pubs = load('publications', list)
seen = set()
for i, p in enumerate(pubs, 1):
    location = f'publications.json entry {i}'
    if not isinstance(p, dict):
        fail(f'{location} must be an object.')
        continue
    slug = p.get('slug', '')
    if not isinstance(slug, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        fail(f'{location}: invalid slug.')
    if slug in seen:
        fail(f'{location}: duplicate slug {slug!r}.')
    seen.add(slug)
    if p.get('status') not in statuses:
        fail(f'{location}: choose a recognized research status.')
    if not p.get('title') or not p.get('summary'):
        fail(f'{location}: title and summary are required.')
    for key in ('image', 'url', 'doi'):
        if not link_ok(p.get(key, '')):
            fail(f'{location}: invalid {key} link.')

for kind in ('academic', 'professional', 'research'):
    d = load(f'cv-{kind}', dict)
    for key in ('title', 'headline', 'summary'):
        if not str(d.get(key, '')).strip():
            fail(f'cv-{kind}.json missing {key}.')
    for key in ('education', 'experience', 'research', 'projects'):
        if not isinstance(d.get(key, []), list):
            fail(f'cv-{kind}.json {key} must be a list.')
    if not link_ok(d.get('pdf', '')):
        fail(f'cv-{kind}.json pdf must be a hosted HTTP(S) URL or existing local file.')

if errors:
    for error in errors:
        print('ERROR:', error)
    raise SystemExit(f'{len(errors)} content error(s) detected.')
print(f'PASS — {len(projects)} project(s), {len(pubs)} research record(s), 3 CV formats and profile validated.')
