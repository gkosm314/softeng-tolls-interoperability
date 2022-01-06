In order to run the scripts using django settings (eg group_creation.py)
we need to have access to those settings

So they must be run redirected to manage.py shell like this:

`
scripts$ python3 ../src/manage.py shell < group_creation.py
`

here running from the scripts directory