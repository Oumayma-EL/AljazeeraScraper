# Not important section to read
The project from the beginning to the end was an amazing adventure specially the errors (coding is not that simple)
# This is important 
The project works only on Aljazeera website.
<br>
The project has 2 files : 
* **moduleScraping.py** which is based on the beautifulsoup and requests only to scrape the latest articles of the current day 
* **modulesScrapingHistoricalArticles.py** based on beautifulsoup and selenium to scrape the historical data from the Aljazeera website with automating the process 

### The most magical part about the project is that you can customize the code for your own needs based on :
* What type of articles (Categories: economy, sports, news...) and the amount of data you want to scrape from the site, and based on your choice you will pick only one file from the two files present in the repository.
* You can choose the categories and also the number of categories you want to have in your CSV file.
# Instructions on how to use 
* You can use the requirements.txt but to be more precise the libraries used are : lxml, selenium (only for the second file if it is the aimed one), Beautifulsoup, requests, pandas and csv.
* Other thing to mention : I used the chromeDriver.exe in the second file for the purpose of using selenium you can find the link for all the versions to download [*here*](https://chromedriver.chromium.org/downloads), pick the one that matches the version of your google Chrome (preferred)
* The commands used to install the libraries for windows (Common libraries for the 2 files):
```Python
pip install lxml
```
```Python
pip install beautifulsoup4
```
```Python
pip install requests
```
```Python
pip install pandas
```
* The commands used to install the required libraries specific only to the second file (moduleScrapingHistoricalArticles.py) :
```Python
pip install selenium
```
```Python
pip install webdriver-manager
```
### *After installing the requirements and trying to run the file of your choice, you may encounter some errors, just be patient and try tp solve them !*

# Overview of the program execution :
If everything is set up correctly, the execution must look like this :
<br>
<br>    
![scraping1](https://user-images.githubusercontent.com/76720983/207116178-34e1c54e-5c5c-45a1-a403-7a345cd5b65c.png)
<br />
<br>
Then you can choose one category. 
And you can customize the number of categories in the function **aggragate_all()** : You can choose the number of categories, so the prompt will appear until choosing all the categories (an example for 3 as an argument for the fucntion is below)
<br/>
<br>
![scraping2](https://user-images.githubusercontent.com/76720983/207117254-e795ada4-190a-447e-8532-3e732bbc1bc3.png)
<br/>
<br/>
You will see the same prompt for the 2 files even if they are different cases of use.
The only difference is in the function *extract_links_from_link_category()* which is programmed differently :
* For extracting just the newest articles in a specific category in a specific day i used just Beautifulsoup.
* For having a large dataset of articles you use the moduleScrapingHistoricalArticles.py where the function *extract_links_from_link_category()* uses selenium to automate the click on the **Show more** button to have access to older articles and then the other functions manage all this and give you a CSV file with 3 attributes the category, the title of the article, and the content of the article at the end.
<br>

**Note** : You can access more articles by changing the **number_of_clicks** variable inside the same function, the bigger the number, the largest your dataset will be
<br>
**Note** : The csv files in the repository are examples of the output of the program.
# At the end 
#### Feel free to fork and add features to the program and enjoy seeing the browser automated and the clicks made without actually clicking!!
