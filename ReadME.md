Instructions to use GitHub:
https://www.geeksforgeeks.org/how-to-upload-project-on-github-from-pycharm/

This project demonstrates how to use the datatables add in along with data from SQL Server & a simple REST API.

The "init_SQLServer.py" file has a the code for using SQL Server as a data source and uses the "PriceSearch.html" template.

The "initREST.py" file has a the code for using SQL Server as a data source and uses the "BooksRestAPI.html" template.

The "init_SQLite.py" file has a the code for using SQL Server as a data source and uses the "BooksSQLLite.html" template.

To use this in practice, you would select one of the options and remove the unecessary files.


The "queryService.py" file has a the code for using a REST API as a data source and uses the "Books.html" template.
Note: the REST API is a seperate project that is deployed on my computer for testing.
This has been placed in another repository called "REST_API" - this can be found at:
https://github.com/kesmith21/REST_API

To add requirements file, enter "pip freeze > requirements.txt" at the terminal prompt.
Here's a link to a good tutorial on how to clone an app to PythonAnywhere:
https://www.youtube.com/watch?v=5jbdkOlf4cY&t=8s