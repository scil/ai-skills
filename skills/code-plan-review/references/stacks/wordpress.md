# Binding: WordPress (sites audited from outside and with WP-CLI, and plugins built on core APIs)

How the tree's nodes show up when a plan checks or changes WordPress sites. Load this file when a plan names WordPress, WP-CLI, `wp-config.php`, or `wp-content/`. Checked against WordPress 7.1 and WP-CLI 2.x (2026-10).

Each entry: **shows up as** · **look for** · **fix**.

## L · Logical

**L5.1: an empty environment variable counts as a set one.**
- *Shows up as:* a Compose file passes a provider key with `KEY: ${KEY:-}`. If the host has no key, the container gets an empty string. The AI Client treats only `false` from `getenv()` as unset (`wp-includes/php-ai-client/src/Providers/ProviderRegistry.php:438-439`). It counts the provider as configured and sends a request with no key.
- *Look for:* `${VAR:-}` or `VAR: ""` on a variable that a `{PROVIDER_ID}_API_KEY` lookup reads. Also look for a "no key" test that starts the container with the variable present.
- *Fix:* pass the variable by name in list form (`- ANTHROPIC_API_KEY`). Test the no-key state and record the outbound HTTP hosts. The list must be empty.

**L5.1: an ID of 0 means the current post.**
- *Shows up as:* a `post_type_link` filter calls `get_permalink()` with an ID from meta. If the meta is missing, the ID is 0, and `get_post( 0 )` returns the global `$post`. The global is often that same post: on its own page, in its edit screen and in REST responses. Then the filter calls itself until PHP runs out of stack, and the visitor gets a white screen or a 500. On other pages the filter returns the link of the global post.
- *Look for:* `get_permalink`, `get_post` or `get_the_title` on an ID that a lookup can return as 0. Examples are `(int)` of missing meta and `absint` of empty input. The risk is highest inside a filter on the same post type.
- *Fix:* return the unfiltered value early for an ID of 0 or less. Test the filter on a post with no meta, with the global `$post` set to that post.

## D · Development

**D5.1: an optional input object rejects no input.**
- *Shows up as:* an ability has an object `input_schema` with no required field and no top-level `default`. The plan says "each input is optional" or "takes no input". A GET request to its run route with no `input` returns 400 `ability_invalid_input` ("input is not of type object").
- *Look for:* `'type' => 'object'` in `input_schema` with no `'default'` at the same level, on an ability that a caller can run with no input.
- *Fix:* add a top-level `'default' => array()`. Checked on WordPress 7.1.4. Test the run route with no input, not only `execute( array() )`.

**D5.3: the run route of the Abilities API needs no signed-in user.**
- *Shows up as:* a plan sets `permission_callback` to `__return_true` because "the REST routes still need a signed-in user". The list and item routes check `read` and return 401 with no user (`class-wp-rest-abilities-v1-list-controller.php:181`, `:193`). The run route calls only the permission callback of the ability, so an anonymous request returns 200.
- *Look for:* `__return_true` on an ability with `show_in_rest`. Also look for a test that sends a request with no user only to the list route.
- *Fix:* state in the plan who can run each ability. To require a signed-in user, use `current_user_can( 'read' )`. Test each route with no user, and test `execute()` as a user with the capability.

## O · Operations

**O1.1: uninstall reaches only the data that someone listed.**
- *Shows up as:* `uninstall.php` deletes a typed list of options and transients. Later code adds options, transients and cron events that the list never gains. No deactivation hook clears the cron events, so WP-Cron keeps them after the plugin is off. One audit found 5 options, 1 transient and 2 cron hooks missing.
- *Look for:* option and transient names typed as strings in `update_option`, `set_transient` and `wp_schedule_event` that `uninstall.php` does not name. Also look for a `wp_schedule_event` with no `wp_clear_scheduled_hook` in a deactivation hook.
- *Fix:* define each option name once as a constant that `uninstall.php` also reads. Clear every scheduled hook in `register_deactivation_hook` and in uninstall. A test compares the prefixed names that the code writes with the names that uninstall deletes.

## P · Process

**P6.2 — an anonymous check passes on a site that serves nothing.**
- *Shows up as:* a check that requests a page anonymously and passes on "not visible" (a draft or private post, a forbidden URL) runs against a site whose every PHP page fails with HTTP 500 — for example PHP-FPM runs as `www-data` while `wp-config.php` is `640` and owned by the site user. On a test target this hides whether the check can ever fail.
- *Look for:* a pass condition that is "not 200" instead of a list of accepted codes; no request that must answer 200 (the home page) in the same run.
- *Fix:* accept only named codes (401, 403, 404, a redirect to `wp-login.php`); a 5xx or no answer is "error", never "pass" or "fail"; the test target runs PHP as the site user and the suite requests a known-good page first.

**P6.4 — default themes are not the theme directory's build.**
- *Shows up as:* an integrity check compares a bundled default theme (`twenty*`) with `downloads.wordpress.org/theme/<name>.<version>.zip`; the copy shipped inside the core package has the same version number but a different `style.css` header (`Tested up to`), a different `readme.txt`, and, in installs from the core archive, some long font file names cut short. Every clean site reports the theme as modified.
- *Look for:* themes whose installed copy came from the core package, compared as if they came from the theme directory.
- *Fix:* compare only the PHP files of bundled themes (or compare them with the core checksums, which list `wp-content/themes/` files) and say so in the result; run the check once on a fresh install before trusting a "modified".

## O · Operations

**O2.1: the ACF JSON save path applies to every field group.**
- *Shows up as:* a plugin keeps its field group under version control with `add_filter( 'acf/settings/save_json', ... )`. That filter sets the save path of every field group, so a group that the site owner makes in wp-admin is also written into the plugin folder. On a served site that folder is release code.
- *Look for:* `acf/settings/save_json` with no `/key=`, `/name=` or `/type=` suffix.
- *Fix:* use `acf/settings/save_json/key=group_<id>` for each group that the plugin owns (ACF 6.2 and later). A test applies the general filter and expects the default path.
