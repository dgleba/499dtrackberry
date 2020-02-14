# Notes


# error

```
albe@pmdsdata7:/srv/file/test/472dkrcollection/499d-django$ docker-compose run --rm djan python manage.py collectstatic

You have requested to collect static files at the destination
location as specified in your settings.

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes
Traceback (most recent call last):
  File "manage.py", line 21, in <module>
    main()
  File "manage.py", line 17, in main
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/__init__.py", line 381, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.7/site-packages/django/core/management/__init__.py", line 375, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/base.py", line 323, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/base.py", line 364, in execute
    output = self.handle(*args, **options)
  File "/usr/local/lib/python3.7/site-packages/django/contrib/staticfiles/management/commands/collectstatic.py", line 188, in handle
    collected = self.collect()
  File "/usr/local/lib/python3.7/site-packages/django/contrib/staticfiles/management/commands/collectstatic.py", line 114, in collect
    handler(path, prefixed_path, storage)
  File "/usr/local/lib/python3.7/site-packages/django/contrib/staticfiles/management/commands/collectstatic.py", line 342, in copy_file
    if not self.delete_file(path, prefixed_path, source_storage):
  File "/usr/local/lib/python3.7/site-packages/django/contrib/staticfiles/management/commands/collectstatic.py", line 249, in delete_file
    if self.storage.exists(prefixed_path):
  File "/usr/local/lib/python3.7/site-packages/django/core/files/storage.py", line 310, in exists
    return os.path.exists(self.path(name))
  File "/usr/local/lib/python3.7/site-packages/django/contrib/staticfiles/storage.py", line 44, in path
    raise ImproperlyConfigured("You're using the staticfiles app "
django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.
albe@pmdsdata7:/srv/file/test/472dkrcollection/499d-django$

```
