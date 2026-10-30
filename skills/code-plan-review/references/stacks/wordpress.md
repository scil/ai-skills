# Binding: WordPress (sites as audited from outside and with WP-CLI)

How the catalog's questions show up when a plan checks or changes WordPress sites. Load this file when a plan names WordPress, WP-CLI, `wp-config.php`, or `wp-content/`. Checked against WordPress 7.1 and WP-CLI 2.x (2026-10).

Each entry: **shows up as** · **look for** · **fix**.

## K. A pipeline judges input

**K2.2 — an anonymous check passes on a site that serves nothing.**
- *Shows up as:* a check that requests a page anonymously and passes on "not visible" (a draft or private post, a forbidden URL) runs against a site whose every PHP page fails with HTTP 500 — for example PHP-FPM runs as `www-data` while `wp-config.php` is `640` and owned by the site user. On a test target this hides whether the check can ever fail.
- *Look for:* a pass condition that is "not 200" instead of a list of accepted codes; no request that must answer 200 (the home page) in the same run.
- *Fix:* accept only named codes (401, 403, 404, a redirect to `wp-login.php`); a 5xx or no answer is "error", never "pass" or "fail"; the test target runs PHP as the site user and the suite requests a known-good page first.

**K2.3 — default themes are not the theme directory's build.**
- *Shows up as:* an integrity check compares a bundled default theme (`twenty*`) with `downloads.wordpress.org/theme/<name>.<version>.zip`; the copy shipped inside the core package has the same version number but a different `style.css` header (`Tested up to`), a different `readme.txt`, and, in installs from the core archive, some long font file names cut short. Every clean site reports the theme as modified.
- *Look for:* themes whose installed copy came from the core package, compared as if they came from the theme directory.
- *Fix:* compare only the PHP files of bundled themes (or compare them with the core checksums, which list `wp-content/themes/` files) and say so in the result; run the check once on a fresh install before trusting a "modified".
