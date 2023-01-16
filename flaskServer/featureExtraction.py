import csv
from urllib.parse import urlparse
import ipaddress
import sys
import re
import tldextract as tld


url_dict = {}


#--------- Feature Extraction Functions -----------------------------------------------

#Calls each of the functions which extracts specific features from the given URL
def extract_features(url, brandlist):
    global url_dict
    
    url_dict = {}
    length_of_url(url)
    length_of_url_sections(url)
    
    num_of_special_characters_in_URL(url)
    num_of_special_characters_in_domain(url)
    num_of_special_characters_in_path(url)
    num_of_special_characters_in_query(url)  
    
    num_of_digits_in_netloc(url)
    num_of_digits_in_path(url)
    
    check_for_brands_in_path(url, brandlist)

#-------------------- Compleated Feature Extraction Functions ----------------

#Counts the entire length of the URL. Outputs count to the "Entire URL Lenght" key in url_dict.
def length_of_url(url):
    url_dict['Entire URL Length'] = len(url)


#Counts the number of special characters in the URL. Outputs count to the "Number of 'variable' in URL" key in url_dict.
def num_of_special_characters_in_URL(url):
    for i in [".", "-", "_", "/", "?", "=", "@", "&", "!", "%20", "~", "+", "*", "#", "$", "%", "%2C"]:
        url_dict["Number of " + i + " in URL"] = url.count(i)


#Counts the numbers of special characters in the URL path. Outputs count to the "Number of 'variable' in Path" key in url_dict.
def num_of_special_characters_in_path(url):
    url_parsed = urlparse(url)
    path = getattr(url_parsed, "path")

    for i in [".", "-", "_", "/", "?", "=", "@", "&", "!", "%20", "~", "+", "*", "#", "$", "%", "%2C"]:
        url_dict["Number of " + i + " in Path"] = path.count(i)


#Counts the numbers of special characters in the URL domain. Outputs count to the "Number of 'variable' in domain" key in url_dict.
def num_of_special_characters_in_domain(url):
    tld_parsed = tld.extract(url)
    domain = tld_parsed.domain

    for i in [".", "-", "_", "/", "?", "=", "@", "&", "!", "%20", "~", "+", "*", "#", "$", "%", "%2C"]:
        url_dict["Number of " + i + " in Domain"] = domain.count(i)


#Counts the numbers of special characters in the URL query. Outputs count to the "Number of 'variable' in Query" key in url_dict.
def num_of_special_characters_in_query(url):
    url_parsed = urlparse(url)
    query = getattr(url_parsed, "query")

    for i in [".", "-", "_", "/", "?", "=", "@", "&", "!", "%20", "~", "+", "*", "#", "$", "%", "%2C"]:
        url_dict["Number of " + i + " in Query"] = query.count(i)


#Check the length of each section of the URL. Outputs length to the "Number of 'variable' in URL" key in url_dict.
def length_of_url_sections(url):
        url_parsed = urlparse(url)
        for i in ["netloc", "path", "query"]:
            url_dict["Length of " + i] = len(getattr(url_parsed, i)) 


#Generates an array from a brandlist and checks if the given URL's path and domain contains any brandnames. Sets the "Brand in Path" key to True or False (Defaults to False)
def check_for_brands_in_path(url, brandlist):
    url_parsed = urlparse(url)
    path = getattr(url_parsed, 'path')
    url_dict["Brand in Path"] = False
      
  
    #Searches the given url path against a regex search of the strings in the brandlist. If a brand is found, sets the key "Brand in Path" to True, this key defaults to False
    for i in range(0, len(brandlist)):
        x = re.search(brandlist[i].lower(), path.lower())

        if x:
            url_dict["Brand in Path"] = True
            break


def check_for_brands_in_netloc(url, brandlist):
    tld_parsed = tld.extract(url)
    url_dict["Brand in Netloc"] = False

    for i in range(0, len(brandlist)):
        x = re.search(brandlist[i].lower(), tld_parsed.domain.lower())

        if x:
            url_dict["Brand in Netloc"] = True
            break
 

#Counts the number of digits in the domain and path. Saves them to seperate entries in the url dictionary
def num_of_digits_in_netloc(url):
    url_parsed = urlparse(url)

    num = sum(d.isdigit() for d in getattr(url_parsed, "netloc"))
    url_dict['Number of Digits in Netloc'] = num

def num_of_digits_in_path(url):
    url_parsed = urlparse(url)

    num = sum(d.isdigit() for d in getattr(url_parsed, "path"))
    url_dict['Number of Digits in Path'] = num


#-----------------------------------------------------------------------------------------

#Parses single URL to features.
def url_to_features(url, brandlist):
    
    extract_features(url, brandlist)
    
    ary = []

    for i in url_dict:
        ary.append(url_dict[i])
    
    return ary


#Generates the brandlist array using Brandlist.txt. 
def generate_brandlist():
    f = open(r"flaskServer/Brandlist.txt", "r")
    #Fills the array brands from the file specified by the variable f
    brands = []
    for i in f:
        brands.append(i.replace(" ", "").strip("\n")) 
    return brands