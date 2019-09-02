#
# 3. FileManager

This chapter describes how the FileManager package grabs data from a spreadsheet, ie a CSV document.

## 3.1. Spreadsheet

The Spreadsheet data type has some methods. Here are all the methods of the Spreadsheet object:

**Spreadsheet(**_file, norm\_headers=None_**)**

* Constructs the spreadsheet into distinguishable headers, columns, and rows. Its member variables are name, headers, 
and _norm\_headers_. The _file_ is the csv file path or name in your local folder. The _norm\_headers_ is a dictionary 
of the original headers paired with your user defined header (ie {Patient Cohort: cohort…}).

Spreadsheet.**name**

* Returns the name of the file as a string.

Spreadsheet.**norm\_headers**

* Returns a list of the normalized headers. Normalized headers are user defined headers which a programmer chooses to 
replace the original headers, without affecting the original file. If no normalized headers were given, then the 
original headers are repeated here. Useful when you want to replace the original headers with shorter header names. 
Yet, still providing you with the same functionality for both header names (ie you can get the column using either the 
norm\_header or original header name).

Spreadsheet.**headers**

* Returns a list of the headers in the spreadsheet. If the headers were normalized, these headers would be the original 
headers.

Spreadsheet.**keys**()

* Gets the headers of the spreadsheet. If the headers were normalized, then the keys are the normalized headers.

Spreadsheet.**exists**(_item=None_)

* Checks if the spreadsheet is nonempty. The optional argument item is to check if a specific _item_ in the spreadsheet 
exists. It returns True if it is found. Else returns False.

Spreadsheet.**has**(_x_)

* Runs a deep search for an item _x_ and return True if it is in the Spreadsheet.

Spreadsheet.**getColumn**(_header_)

* Returns a list of the contents in the column within the _header_ column.

Spreadsheet.**find**(_x_)

* Returns every row in which _x_ is found in.

Spreadsheet.**convertToDict**(_list_)

* Converts a list of the rows in the Spreadsheet into a list of dictionaries with the keys being the associated headers 
and the values being the list in the parameter.

Spreadsheet.**trunc\_text**(_text, length=30_)

* Returns a truncated _text_ with the maximum length being of size _length_. The optional argument length will default 
to the length 30 if not specified.

Spreadsheet.**max\_results**(_num\_results=4_)

* Returns the maximum results in the Spreadsheet. The optional argument limits it to the top 4 maximum results

Spreadsheet\[**int**\]

* Iterates through the spreadsheet from 0 to n - 1. The index starting at 0, where 0 is the first row, and ending at 
n - 1, where n - 1 is the last row in the Spreadsheet. Headers are not included in the output of each row.

Spreadsheet\[**str**\]

* Searches the string in the rows of the Spreadsheet. If the string is in the row of the Spreadsheet, 
then the row is returned. If it occurs in multiple rows, then multiple rows are returned as a list of rows.

Spreadsheet\[**int:int**\]

* You can slice through a Spreadsheet to get a range of rows.

Spreadsheet\[**:-1**\]

* Most slicing operators are available.

**len**(_Spreadsheet_)

* Returns the number of rows in the Spreadsheet.

## 3.1.1 More on Spreadsheet

Here are some examples on how to use the Spreadsheet.  
Constructing the Spreadsheet and using norm headers.
> **\>>>** from Activity.FileManager.Spreadsheet import Spreadsheet  
> **\>>>** NORM_HEADERS = { 'id': 'id', 'Topic': 'topic', 'Date Discussion (Month/Year)': 'date', 'Query Tag': 
'query_tag', 'Patient Query/inquiry': 'query', 'Specific Patient Profile': 'profile', 'Patient Cohort (Definition)': 
'cohort', 'Tumor (T)': 'tumor', 'Tumor Count': 'tumor_count', 'Node (N)': 'node', 'Metastasis (M)': 'metastasis', 
'Grade': 'grade', 'Recurrence': 'recurrence', 'Category Tag': 'category', 'Intervention': 'intervention',
'Associated Side effect': 'side_effects', 'Intervention mitigating side effect': 'int_side_effects',
'Patient Insight': 'insights', 'Volunteers': 'volunteers', 'Discussion URL': 'url', 'HER2': 'HER2', 'HER': 'HER',
'BRCA': 'BRCA', 'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO' }   
> **\>>>** sheet = Spreadsheet(‘insights.csv’, NORM_HEADERS)  

Getting the column with the header 'date' as the norm header.
> **\>>>** sheet\[**'date'**\]  
\['', 'September 1, 2018', 'September 11, 2018', 'November 1, 2015', … \]  

Getting the column with the original header 'Date Discussion (Month/Year)'.
> **\>>>** sheet\[**'Date Discussion (Month/Year)'**\]  
['', 'September 1, 2018', 'September 11, 2018', 'November 1, 2015', … ]  

Truncating text to up to 15 letters maximum.
> **\>>>** sheet.**trunc_text**('Treatment is something people search for after a diagnosis', 15)  
'Treatment is so...'   

Converting a list of rows into their dictionary pairing with the headers.
> **\>>>** results = sheet\[**'Treatment'**\]  
\[\[1', 'July 2015', 'Treatment', 'Patient had …', …\], …, \['99',  …,  'Kriti Bhardwaj, Amira Elfergani',
'https://community.’, '',  '', '', '', ''\], …\]  
> **\>>>** sheet.**convertToDict**(results)  
\[{'id': '1',  'topic': '',  'date': 'July 2015',  'query_tag': 'Treatment',  'query': 'Patient had …', …, 'RO': ''}, 
…, {'id': '99',  'topic': '', …,  'volunteers': 'Kriti Bhardwaj, Amira Elfergani', 'url': 'https://community.’, 
'HER2': '',  'HER': '',  'BRCA': '',  'ER': '',  'HR': ''}, …\]  
