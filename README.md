# OCR_PostAPI_RPA
As part of the Mitutoyo OCR project, I am wrote Python code using Clover OCR's Last API to verify PoC.
(This code can OCR process pdf and png files. Also, the PDF library pdfplumber and
You need to import pandas, a library for controlling Excel, into Python. 
ex.. pip install pdfplumber
ex.. pip install pandas
)

## Enter Clover OCR’s API key value
Please enter a value for null
* api_url = 'null'
* secret_key = 'null'

Please enter the path to the folder where pdf and png format files to be OCR processed are stored.
* directory_path = 'null'

## How to enter field values
And in the keys below, you must write the names of each labeled field in Clover OCR.
* keys = ["",""]
example
keys =  ["작성자", "접수번호", "의뢰자", "형식", "기기번호"]

## result
The OCR processed results are automatically saved in Excel.
excel_path = 'C:\\Users\\seukim\\Downloads\\result.xlsx'
Please modify the Path to determine the storage location.
