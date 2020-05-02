from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com
for x in range(4,33):
    page_url = "https://www.a2oj.com/Ladder"+ str(x) +".html"

    # opens the connection and downloads html page from url
    uClient = uReq(page_url)

    # parses html into a soup data structure to traverse html
    # as if it were a json data type.
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()

    # finds each product from the store page
    containers = page_soup.findAll("a")

    # name the output file to write to local disk
    out_filename = "Data/Ladder"+str(x)+".csv"
    # header of csv file to be written
    headers = "SNo,QueName,QueLink,Contest,QueType \n"

    # opens file, and writes headers
    f = open(out_filename, "w")
    f.write(headers)

    # loops over each product and grabs attributes about
    # each product
    index=1
    for container in containers:
        SNo = index
        QueName = container.string
        QueLink = container.get('href')  
        QueLink = QueLink.replace("problemset","contest")     
        arr = QueLink.split("/")
        lst = len(arr) - 1
        index = index+1  
        QueType = arr[lst]
        arr[lst-1] , arr[lst-2] = arr[lst-2] , arr[lst-1]
        Contest = arr[lst-2]
        QueLink = '/'.join(arr) 
        
        # prints the dataset to console
        print("SNo "+str(index)+ "\n")        
        print("QueName: " + QueName + "\n")
        print("QueLink: " + QueLink + "\n")
        print("Contest: " + Contest + "\n")
        print("QueType: " + QueType + "\n")
        
        
        # writes the dataset to file
        f.write(str(SNo) + ", " + QueName.replace(",", "|") + ", " + QueLink + ", " + Contest + ", " + QueType +"\n")

    f.close()  # Close the file
