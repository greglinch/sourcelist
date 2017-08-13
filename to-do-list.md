# To-do's

* hide foreign key admins from non-superusers

* hide person objects from everyone unless they 
	* approved
	* added the person
	* are the person (based on logged in user email)
	* are a journalist

* log of who viewed a source

* give contributors access to add, but not edit or delete

* how to handle ratings? added directly on the person or added in their own model and then you choose a user to attach it to?
	* use a mgmt cmd to calculate?

* management commands to send emails to 
	* admin
	* user when added
	* user when approved

* add oauth
	* Google
	* Twitter
	* Facebook

* add magiclink login option

* how to handle displaying `approved` (hiding for all but superuser) and `rating` (hiding to sources)?
	* model inheritance? 

* switch city, state, country, timezone, etc to FK fields?
	* advantage: filters wouldn't show all choices for country -- just the ones available

* should org be m2m field? FK?