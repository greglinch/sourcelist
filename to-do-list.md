# To-do for production

* update nginx caching

# To-do for development

* FIX: import issues (currently 4 remaining)

* UPDATE: email used to diversesources@gmail.com

* add `pending`, `reviewed` (redundant with `approved_by_admin` as True?) or `rejected` for admins

* we should add something that says we vet the sources, but journos should also do their due diligence
	* Q: where? about page?

* BUG: required asterisk not appearing in `join` form for `country` although it's required

* BUG: hamburger menu doesn't collapse for responsive view `results.html` 
	* work fine for all others, so probably a JS conflict

* move css to external file under static
	* also move all inlines styles there (e.g. image width for about)

* fix order of fields displayed in `email_user`

* Q: add `-e` flag for `import_csv` command to indicate whether to trigger `email_user`?
	* DOESN'T MATTER bc mgmt cmds called in `post_save` for model

* update admin `index.html` with logic to see if superuser and display all recent actions, else just those of the user 

* DataTables updates
	* setting column width percents to avoid line breaks
	* explore adding stacked view on mobile

* (v2?) add "report this profile" link to send message on `person_detail` page template
	* inaccurate
	* imposter
	* offensive
	* other (explain)

* (v2?) send user a message with their profile and link to update if someone tries to submit a new version
	* would that be spamming? make them click a link to send that message?

* (v2?) include a confirmation link in `email_user` for admin to approve 

* (v2?) write error module to abstract error messages for `except` statements
	* send to G, M or both? or an admin email Google group

* (v2?)  because of `post_save` and view logic, it can take a few seconds to save, so might be best to trigger a saving screen to let user know it's processing and so they don't do anything they're not supposed
	* e.g. `$().submit()` load a screen overlay (using `z-index`?) so user can't do anything until it's done
	* both in admin and on front-end forms
	* NOTE: based on quick testing, it looks like we're ok because of logic to avoid duplicate emails; it just says your account is already created, check email (so not ideal but should be ok)

* how to handle ratings? 
	* require Journalist profile?
	* added directly on the person or added in their own model and then you choose a user to attach it to?
	* ManyToManyField? (only show ones added by that user)
	* use a mgmt cmd to calculate?

* Point domain to the static files
	* needs to be the same exact URL structure as dynamic app

* switch `ConfirmView` responses to `HttpResponseRedirect` to `\thank-you\` page with appropriate context

* email analytics?

* Q: add `_raw` `CharField`s for `org`, `expertise`, `language`, etc and then have admin update the related `M2Mfield`s in admin based on that, which will be what's used for filtering?
	* or figure out a way for submissions to choose/add instead of just only choose (`M2M` displayed) or only add (`CharField` displayed)
	* or do those just not really matter bc will wants filters for TZ and then search whatever else?

* save all the FK'ed fields on person model to flatten the data

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

* hide journo M2M fields from sources

* log of which journalist has viewed a source

* how to handle displaying `approved` (hiding for all but superuser) and `rating` (hiding to sources)?
	* model inheritance? 

* if we do front-end edit urls, change edit link from admin url to live url

* Django bakery to make static files?
	* better to simply use nginx to see caching?
	* https://django-bakery.readthedocs.io/en/latest/gettingstarted.html

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

* for `person_detail`, find a way to loop thru the keys and values that have been limited by `.values()` and ordered a specific way

* set up auth for Facebook
	* https://python-social-auth.readthedocs.io/en/latest/backends/facebook.html#oauth2

* dynamically-generated xml sitemap
	* https://github.com/xaralis/django-static-sitemaps

* highlight current page in the navbar
	* https://stackoverflow.com/a/7665655/217955

* add admin action to batch set `approved_by_admin`

* add @ symbol Bootstrap add-on to imput for Twitter 
	* https://getbootstrap.com/docs/3.3/components/#input-groups-sizing

# QUESTIONS 

* sync IDs across User and Person?

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

* Q: use this for front-end search?
	* https://gregbrown.co/projects/django-simple-search
	* https://github.com/gregplaysguitar/django-simple-search

* Q: switch email content from formatted string in a mgmt cmd to html template?

* Q: add boolean to `User` list display view to indicate that they're tied to a `Person`?
	* also include editable dropdown to add/change the associated `Person`?

# NOTE FOR LATER

https://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models

https://github.com/fajran/django-loginurl

https://docs.djangoproject.com/en/1.11/ref/forms/api/#checking-which-form-data-has-changed

# PUNTING

* limit `status` choices displayed on ModelForm for `JoinView`
	* field includes all, but we'd only want to include `added_by_self` and `added_by_other`

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

