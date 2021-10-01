project uses a sqlite database to cities read data into pandas
reason I chose sqlite was the idea I had of linking the teachings of project number 1 which was in postgresql but chose sqlite for is portability 
-- main site used to reference sqlite syntax is https://www.sqlite.org/lang_datefunc.html since the biggest challenge was understanding how sqlite deals with date columns
this stack overflow page also useful in converting the date format

for the python bit 
	https://www.programiz.com/python-programming/methods/built-in/divmod helped in understanding divmod
	https://www.geeksforgeeks.org/python-pandas-to_numeric-method/ for datataype conversions and various stack overflow pages
	
	this youtube channel also instrumental in showing how to use map and filter
	
	
My approach was to use sql lite as ian initial data source since we've already learnt about database querying in the first project.
Data source loads the info to a pandas dataframe the I use pandas to work out the general statistics