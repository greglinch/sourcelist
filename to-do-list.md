# To-do for production

* update nginx caching

# To-do for development

* add "report this profile" link to send message on `person_detail` page template that includes the URL when sent
	* reasons
		* inaccurate
		* imposter
		* offensive
		* other (explain)
	* DONE types (open in a menu?)
		* someone else, so let us know what's out date and/or submitted updated info
			* DONE also include a link to the other type in case they ended up in the wrong place
			* DONE prepopulate profile id when they come from a profile
				* make that readonly or editable? hide ID, show name
		* me, so send magic link to update profile
	* DONE fix styling
		* horizontal alignment of "return to db" and "report"
		* "report button" dropdown missing example styling
		* input checkboxes should appear to the right of the label
	* DONE handle when there's no REFERRER
		* currently throws an exception, yikes!

* report updated profile: allow admin to click a url w/ params in it to update the admin change form
	* will likely need to override the default view so it grabs params from the URL, such as https://stackoverflow.com/a/49463287/217955

* FIX issue with duplicates and redirects; fixed bc deleted dupes on prod
	* see work started on add-id-to-urls-with-redirect branch

* write migration to create necessary user groups
	* name: change source and add related
	* perms: can change person

* unless it breaks auto-setup of things in Django, rename DetailView to not conflict with the class it inherits

* refactor to make code better
	* switch all URLs to use reverse()
		* TODO: make sure email_user mgmt cmd works

* Host datatables files ourselves (on app server or static server?
	https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css
	https://cdn.datatables.net/responsive/2.2.1/js/dataTables.responsive.min.js
	https://cdn.datatables.net/r/bs-3.3.5/jqc-1.11.3,dt-1.10.10/datatables.min.js

* Update results.html to point to the new location

* update view for setting related user and emailing the user
	* wrap both calls in try/except
	* notify admin if either or both fail: single email for both
	* see commented out code for starting point
	* need to update thank-you template to handle more advanced messaging depending on fail_type

* (in progress) Invite Sources: Link that sends emails to invite others to join
	* Use Facebook? Twitter? Just email?
	* store the information as a draft source object and pre-populate join form?

* add a "Testimonials" style page with success stories instead of just on the about page

* ??? add Patreon https://www.patreon.com/diversesources

* social media display inspiration: https://www.genderavenger.com/
	* for our FB, Tw, IG accounts

* finish Spanish translation of About page

* fix? user is able to see a live page when clicking "view on site" on their person page using the magic link, even if that page doesn't exist

* FIX: search on mobile bc it's out of whack with social icons and hidden in the hamburger menu

* change redirect after social login
	* requires adding a step to the pipeline —- doesn't work just with logic in the template bc it doesn't know whether you're a superuser at that point

* more detailed “about” on home page?

* fix confirmation link issues
	* add fields?
		* confirmation_clicked
		* confirmation_user_agent ???
	* add confirm page instead of clicking link?
	* how do TinyLetter and Mailchimp get around this? bc they just have single confirm links

* IN PROGRESS:  because of `post_save` and view logic, it can take a few seconds to save, so might be best to trigger a saving screen to let user know it's processing and so they don't do anything they're not supposed
	* e.g. `$().submit()` load a screen overlay (using `z-index`?) so user can't do anything until it's done
	* both in admin and on front-end forms
	* NOTE: based on quick testing, it looks like we're ok because of logic to avoid duplicate emails; it just says your account is already created, check email (so not ideal but should be ok)

* upgrade to Django 2.0
	* ran into some issues, so probably best to do this in a separate repo first

* FIX: width of content well of person_detail template runs over horizontally on mobile

* add ability for people to do links with brief comments and titles for their mentioned citations or things that they got because of the database

* FIX: import issues (currently 4 remaining)

* automatically send nudge message to user after X days to remind them they need to confirm their profile

* BUG: required asterisk not appearing in `join` form for `country` although it's required

* FIX BUG: hamburger menu doesn't collapse for responsive view `results.html` 
	* work fine for all others, so probably a JS conflict

* if someone has submitted and gets the "your profile already exists" prompt, give them a button to "Send me link to edit my profile"

* move css to external file under static
	* also move all inlines styles there (e.g. image width for about)

* fix order of fields displayed in `email_user`

* !!! wrap user-facing ForeignKey, OneToOne and ManyToMany fields in `_()` for translation when/if activated !!!
	* https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#model-fields-and-relationships-verbose-name-and-help-text-option-values

* use `from django.utils.translation import ugettext_lazy as _` for `forms.py`?
	* docs say to use for forms, but idk if applicable give our setup (e.g. no hard-coded text in it)

* translating URL patterns
	* https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#translating-url-patterns

* Q: worth fixing edge case URL problems that break?
	* if /sources/ is missing
		* it's redundant anyway, so can probably just remove
	* missing id, but still has extral slash: e.g. /sources//first-last
	* url params with missing ID: e.g. /sources/first-last/?thank-you=true
		* only breaks when ID is missing (e.g. /sources//first-last or /sources/first-last), fine when ID is there and slug is broken/missing
		* https://diversesources.org/sources/580/rocio-acuna-hidalgo//sources/580/rocio-acuna-hidalgo/?social=true

* Q: add `-e` flag for `import_csv` command to indicate whether to trigger `email_user`?
	* DOESN'T MATTER bc mgmt cmds called in `post_save` for model

* update admin `index.html` with logic to see if superuser and display all recent actions, else just those of the user 

* DataTables updates
	* setting column width percents to avoid line breaks
	* explore adding stacked view on mobile 

* abstract the column list in `results.html`, such as:
```
{% for field in field_list %}
    <th>{{ field }}</th>
{% endfor %}
```

* add to base.html? but make sure you can override first (e.g. with specific pages titles)

```
{% block header %}

{% endblock %}
```

* ? Create images with Python PIL and Pillow and write text on them ?
	https://code-maven.com/create-images-with-python-pil-pillow

* (v2?) write error module to abstract error messages for `except` statements
	* send to G, M or both? or an admin email Google group

* how to handle ratings? 
	* require Journalist profile?
	* added directly on the person or added in their own model and then you choose a user to attach it to?
	* ManyToManyField? (only show ones added by that user)
	* use a mgmt cmd to calculate?

* Q: add `_raw` `CharField`s for `org`, `expertise`, `language`, etc and then have admin update the related `M2Mfield`s in admin based on that, which will be what's used for filtering?
	* or figure out a way for submissions to choose/add instead of just only choose (`M2M` displayed) or only add (`CharField` displayed)
	* or do those just not really matter bc will wants filters for TZ and then search whatever else?

* front-end search should be additive, not start over
	* e.g. if already one or more params, just append to query string (need to get that with JS?)

* UPDATE: front-end form
	* Q: include checkbox for "not this person?"
		* and then `$().show()` optional addtl fields for the submitter's name and email?
		* https://stackoverflow.com/questions/13550515/django-add-extra-field-to-a-modelform-generated-from-a-model
	* Q: let a user edit their info on that form instead of admin?
	* Q: pass updated workflow status to that form via URL and hide that field from displaying?
	* however that form is populated, make sure it's not just on things other people could guess; e.g. make sure it's... 
		* a unique string different from system ID
		* is combined with user email?

* consider switching `set_related_user` to look up based on the `id` of a `Person` rather than the `email_address` to avoid possible duplicates
	* altho that should be an issue bc there wouldn't be a duplicate `User` -- it would just update
	* and I could add validation to make sure `email_address` doesn't already exist
	* overall, might still be easier to just use `id`

* for `person_detail`, find a way to loop thru the keys and values that have been limited by `.values()` and ordered a specific way

* dynamically-generated xml sitemap
	* https://github.com/xaralis/django-static-sitemaps

* highlight current page in the navbar
	* https://stackoverflow.com/a/7665655/217955

* add admin action to batch set `approved_by_admin`

* add @ symbol Bootstrap add-on to imput for Twitter 
	* https://getbootstrap.com/docs/3.3/components/#input-groups-sizing

# QUESTIONS 

* save all the FK'ed fields on person model to flatten the data?

* add ('Prof.', 'Prof.'), to PREFIX_CHOICES, but then do we need all variations?

* sync IDs across User and Person?

* Django bakery to make static files?
	* better to simply use nginx to see caching?
	* https://django-bakery.readthedocs.io/en/latest/gettingstarted.html
	* then point domain to the static files
	* needs to be the same exact URL structure as dynamic app

* email analytics?

* Q: show a source the `Person` or `Source` model to edit their info?

* Q: add a role for `submitter` (e.g. PIO, PR person)
	* maybe, but not yet

* Q: how to associate new Person if there are multiple Users for that person? 

* Q: should the username just be their email address? bc that's our unique ID

* Q: create a model for proposed changes to a Person?
	* then the user or the admin could accept or decline these
	* use inheritance to just inherit the fields, but make it a separate table that doesn't push back to parent table (if possible)

* Q: store what emails have been sent to a user?
	* Emails model? So we can track that?

* Q: add new statuses if a Person has been updated or use existing flow?

* Q: alternative setup
	* sources/submitters can submit/view their entry only on the front-end
	* journalists can only view `role='source'` in the admin for a model called `Sources` that mirrors `Person` but only shows certain fields (e.g. not status, etc)

* Q: another alternative setup
	* same as above, but when you editing + re-submit an entry, it gets a new id and override the old one; options for override
		* make the other one inactive/unpublish
		* delete the old one so only the new one exists

* Q: should org be m2m field? FK?

* Q: contact form for site to track which journalists message which sources?
	* where did we end up on that during earlier discussion?

* Q: how to handle special characters in names? 
	* e.g. https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string

* Q: switch email content from formatted string in a mgmt cmd to html template?

* Q: add boolean to `User` list display view to indicate that they're tied to a `Person`?
	* also include editable dropdown to add/change the associated `Person`?

* Q: add django-ckeditor?


# NOTE FOR LATER

https://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models

https://github.com/fajran/django-loginurl

https://docs.djangoproject.com/en/1.11/ref/forms/api/#checking-which-form-data-has-changed

# PUNTING

* limit `status` choices displayed on ModelForm for `JoinView`
	* field includes all, but we'd only want to include `added_by_self` and `added_by_other`

* hide journo M2M fields from sources

* log of which journalist has viewed a source

* how to handle displaying `approved` (hiding for all but superuser) and `rating` (hiding to sources)?
	* model inheritance? 

* if we do front-end edit urls, change edit link from admin url to live url

* include a confirmation link in `email_user` for admin to approve
	* probably won't do bc admin must vet the user

* search form/page
	* https://simonwillison.net/2017/Oct/5/django-postgresql-faceted-search/
	* https://select2.org/getting-started/basic-usage
	* https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/search/

* switch city, state, country, timezone, etc to FK fields?
	* advantage: filters wouldn't show all choices for country -- just the ones available
	* NOTE: be sure to save them on self

* in admin, hide person objects from everyone unless they 
	* approved by user
	* approved by admin
	* added the person
	* are the person (based on logged in user email)
	* are a journalist

* set up auth for Facebook
	* https://python-social-auth.readthedocs.io/en/latest/backends/facebook.html#oauth2

# COMPLETED

* add oauth
	* Google
	* Twitter
	* Facebook

* setup auth for 
	* Twitter
	* Google

* how to how handle User and Person models?
	* tie them together by email?
	* SOLUTION: save_model for PersonAdmin will associate

* addtl fields?
	* created_by (User who created the profile)
	* related_user (User the profile relates to)

* status drop-down instead (or in addition to?) of `approved` boolean
	* added
	* confirmed by user
	* confirmed by admin

* WONT ADD: add boolean for add form to indicate whether you're adding yourself or someone else
	* status handles

* give new `User` necessary permissions 

* management command triggered `post_save` to send emails to user when added by self or another with ability to edit

* fix `User` not associated with `Person` until second `save_model` bc they're created on first `save_model`
	* we need this so the auth token is generated for the related `User`
	* SOLUTION: it needed a `.save()` call on the association

* hide foreign key admins from non-superusers
	* SOLUTION: done via only giving `add` perms and not `change` perms

* add magiclink login option
	* option 1 (tried) http://www.idiotinside.com/2016/11/13/django-slack-magic-link-passwordless-login/
	* option 2 (not tried) https://github.com/fajran/django-loginurl

* limit emails sent to user
	* currently it's every `post_save`
	* SOLUTION: before calling mgmt cmd, check if `instance.created == instance.updated`

* add logic to `save_model` for setting workflow to see if current user matches user being added
	* if not and not superuser, set to added by other
	* if not and is super, set to added by admin

* show the info submitted in the email 

* add Bootsrap

* add a front-end form for submitting new sources

* write import script (mgmt cmd) for csv of existing sources

* add views
	* submission form
	* about

* update a `User` based on an update to a `Person`
	* code is written, but doesn't update

* add type of scientist to all necessary places (admin, submission form, email sent to source, etc.)

* switch to postgres so we can utilize more advanced search options
	* https://docs.djangoproject.com/en/1.11/topics/db/search/#a-database-s-more-advanced-comparison-functions

* include a confirmation link in `email_user` for user to approve 

* set `source` as the deafult `role` for a `Person`

* add logic to `Person` model save method to check if one of the `approved` booleans is True, then set the `status` accordingly

* update `results.html` template to output a table

* use DataTables Bootstrap version for search/display
	* MABI is ok with that for v1

* only display `Person` objects that have are both `approved_by_user` and `approved_by_admin`
	* filter the queryset in `views`

* switch to class-based views, especially for `join` and `contact`
	* https://docs.djangoproject.com/en/1.11/topics/class-based-views/intro/

* add link to the detail view in `results.html`

* add detail view for sources

* FIX: `status` not being set automatically, despite same (?) code in admin `save_model` for Person class
	* Solution: add new choice just called `added` and set it in `Person` save method if there's none

* add way to handle if someone submits a duplicate
	* currently, it throws an exception from the `email_user` mgmt cmd bc `get()` only work with unique item
	* YES --> possible solution: add logic to see if the email address already exists
	* NO --> possible solution: override existing entry with new entry? but that could be problematic if a third-party is submitting and the info is incorrect

* approve user on the part of the user
	* NOTE: if we can't have approval via email yet, then make them confirm in the admin (e.g. using existing `approved_by_user` boolean, which will need to trigger in the method an update of the `status`)
	* Q: or is this is a good reason to separate all the `status` options to their own booleans? not sure

* include `sources/` before `slug` for urls?
	* would help avoid potential issues with any main pages that look like slugs (e.g. `/thank-you`)

* UPDATE: Bootstrap design

* hide permissions and other fieldsets a non-superuser shouldn't have access to in the `UserAdmin`
	* https://stackoverflow.com/questions/2297377/how-do-i-prevent-permission-escalation-in-django-admin-when-granting-user-chang
	* e.g. http://127.0.0.1:8000/admin/sources/person/17/change/?method=magic&url_auth_token=AAAADxvpRtr-cHETXIC5RyZf_E4:1e6I0F:1zV89aib1meRK5akQMaUkaWinYA

* finish detail view for sources

* Q: use AWS or personal hosting space? 
	* AWS

* rename app in Google API console so it matches if people login with oauth

* PROD: create auth groups for permissions (mimic local version)

* add Google Analytics

* PROD: Let's Encrypt `certbot`
	* requires non-AWS domain for EC2
	* requires workaround for personal hosting

* disable all non-main allowed hosts after testing is done

* starter, statically-generated xml sitemap

* change Bootstrap and related files to CDN versions
	* or host them ourselves

* add credits: Mollie, Greg, Nacin, Kevin

* add `return to database` link on `person_detail`

* 404 page
	* probably want to redirect to 404 page
	* probably don't want these
	* https://stackoverflow.com/questions/14286732/how-do-i-redirect-from-a-django-detailview-when-the-specified-object-doesnt-exi
	* https://docs.djangoproject.com/en/1.11/topics/http/views/#the-http404-exception

* favicon
	* https://gist.github.com/asmallteapot/2038673

* Q: add `preferred_pronoun` field?

* FIX: timezone handling for `import_csv` and, after fixed locally, re-import those on prod

* add ability to show "please confirm your profile in email" text if coming from `join.html` -- but not from `contact.html`

* add fields and icons for text, audio and video media
	* are you comfortable with or have experience the following?

* BUG: received email three times after submitting join form

* resize width of input boxes for person note and contact message 

* PROD IMPORT: make sure everyone doesn't receive a message until we need them (for updating their info)

* social media icons (in top-right of navbar? in footer?)
	* https://www.facebook.com/DiverseSources/
	* https://twitter.com/DiverseSources
	* https://www.instagram.com/diversesources/

* social metadata

* add advisory board section to about page

* abstract pages and all text that we want to change to be control by a `Page` model or something we can do that all via the admin and not the code each time 

* make website field required

* add
	* terms of service (part of about?)
	* footer: started but mostly empty

* we should add something that says we vet the sources, but journos should also do their due diligence
	* Q: where? about page?

* UPDATE: email used to diversesources@gmail.com

* translate template text with HTML in it
	* use blocktrans template tag

* translate text stored in the database (e.g. About page)
	* idea: since it's HTML, just use a hidden div and toggle?
	* solution: JS toggle w/ hidden div for About page

* add `pending`, `reviewed` (redundant with `approved_by_admin` as True?) or `rejected` for admins
	* accomplished by adding a new `declined_by_admin` field

* move video/audio/text icons to bottom of `person_detail` template

* in `results.html` template, update
		<a href="{% url 'source' slug=result.slug %}">
	to
		<a href="{{ result.get_absolute_url }}">

* SEARCH ENGINE: need to be able to search across all fields
	* django-watson does the trick
	* make sure watson search properly filters (approved by admin + user) results
		* done in apps.py
	* add post-save method to trigger `buildwatson`
		* done in models.py
	* Q: use this for front-end search?
		* https://gregbrown.co/projects/django-simple-search
		* https://github.com/gregplaysguitar/django-simple-search

* add recaptcha to contact form

* update contact form field based on selecting an option:
	* general contact
	* bug report
	* share your story (journalist)
	* share your story (source)

* add a "Share Your Story" link to nav for testimonials and have a form -- either the contact form or something more specific

* add plus sign to template `person_detail.html` for timezone

* update "return to database" to be a "return to results" if coming from a search result page

* update `ConfirmView` and add `confirm.html` template to improve the confirmation experience

* WONT DO: send user a message with their profile and link to update if someone tries to submit a new version
	* would that be spamming? make them click a link to send that message?
	* have a better, more purposeful and less spammy solution above

* add custom filter for emails addresses and phone numbers to convert special characters to HTML entities as a countermeasure to simple scrapers looking for those patterns

* update Twitter help text

* fix "back to results" button for pagination
	- solution: `stateSave: true,` uses local storage

* fix datatables filter

* upgrade Django

* fix django-magic-link
	- removed django from reqs bc it was 1.10.x
	- didn't work properly with Django 2.1 until upgrading django-seasame from 2.1 to 2.4 in the sourcelist reqs

* add ID to url to avoid duplicate or same name issues; with redirects for...
	* SOMEWHAT DONE: messed up name goes to canonical
	* DONE: old urls go to canonical
	* DONE: /sources goes to homepage

* FIX: 500 error when trying to "view on site" in any model
	* update get_absolute_ur? 
		* reverse('source', args=[self.slug, self.id])
	* solution: change it to kwargs like in the recent view updates
