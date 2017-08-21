# To-do's

* IN PROGRESS: add a front-end form for submitting new sources
	* include dropdown for who submitted (`self`, `submitter`)
		* not going to do this for now
	* Q: include more info about submitter if `other`/`submitter` (e.g. name and email)
	* Q: let a user edit their info on that form instead of admin?
	* Q: pass updated workflow status to that form via URL and hide that field from displaying?
	* however that form is populated, make sure it's not just on things other people could guess; e.g. make sure it's... 
		* a unique string different from system ID
		* is combined with user email?

* IN PROGRESS: management command triggered `post_save` to send emails to 
	* user when added by self or another
		* show the info submitted in the email and include a link to approve or edit
		* confirm link / edit info (if needed)

* limit emails sent to user
	* currently it's every `post_save`

* add logic to see if current user matches user being added
	* if not and not superuser, set to added by other
	* if not and is super, set to added by admin

* management commands to 
	* approve user on the part of the user
	* approve user on the part of the admin
	* NOTE: should they be the same and just have an args and condtl to have differences?
	* update a `User` based on an update to a `Person`

* fix user not associated until second `save_model` bc they're created on first `save_model`
	* or could the solution be forcing a save on approve?
	* BETTER SOLUTION: post_save signal mgmt cmd?

* because of `post_save`, it can take a few seconds to save, so might be best to trigger a saving screen to let user know it's processing and so they don't do anything they're not supposed
	* e.g. `$().submit()` load a screen overlay (using `z-index`?) so user can't do anything until it's done

* add magiclink login option
	* option http://www.idiotinside.com/2016/11/13/django-slack-magic-link-passwordless-login/
	* option https://github.com/fajran/django-loginurl

* add social logins to `/admin` (a la DocPub)

* hide foreign key admins from non-superusers

* hide person objects from everyone unless they 
	* approved by user
	* approved by admin
	* added the person
	* are the person (based on logged in user email)
	* are a journalist

* hide journo M2M fields from sources

* log of who viewed a source

* how to handle ratings? 
	* added directly on the person or added in their own model and then you choose a user to attach it to?
	* ManyToManyField? (only show ones added by that user)
	* use a mgmt cmd to calculate?

* write import script (mgmt cmd) for csv of existing sources

* how to handle displaying `approved` (hiding for all but superuser) and `rating` (hiding to sources)?
	* model inheritance? 

* switch city, state, country, timezone, etc to FK fields?
	* advantage: filters wouldn't show all choices for country -- just the ones available
	* NOTE: be sure to save them on self

* should org be m2m field? FK?

* save all the FK'ed fields on person model to flatten the data

* set up auth for Facebook
	* https://python-social-auth.readthedocs.io/en/latest/backends/facebook.html#oauth2

* add views
	* IN PROGRESS: submission form
	* terms of service
	* about
	* search page?

* rename app in Google so it matches if people login with oauth

# To-dos on live version

* create auth groups for permissions (add/edit sources et al)

# QUESTIONS 

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