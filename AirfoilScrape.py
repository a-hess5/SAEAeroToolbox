import math

from bs4 import BeautifulSoup
import requests
import csv

file_path = "foil_data_new1.csv"
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write header row (optional)
    header = ["Name", "Data Url", "CL- 0 Deg Alpha", "CD- 0 Deg Alpha", "CL/CD- 0 Deg Alpha", "CL- 3 Deg Alpha", "CD- 3 Deg Alpha", "CL/CD- 3 Deg Alpha", "CL- 5 Deg Alpha", "CD- 5 Deg Alpha", "CL/CD- 5 Deg Alpha", "CL- 7.5 Deg Alpha", "CD- 7.5 Deg Alpha", "CL/CD- 7.5 Deg Alpha", "CL- 10 Deg Alpha", "CD- 10 Deg Alpha", "CL/CD- 10 Deg Alpha", "Maximum CL"]
    writer.writerow(header)

pageNum = 0

while (pageNum < 164):
#while (pageNum < 3):
    starturl = "http://airfoiltools.com/search/index?m%5BtextSearch%5D=&m%5BmaxCamber%5D=&m%5BminCamber%5D=&m%5BmaxThickness%5D=&m%5BminThickness%5D=&m%5Bgrp%5D=&m%5Bsort%5D=1&m%5Bpage%5D=" + str(pageNum) + "&m%5Bcount%5D=1638"
    page = requests.get(starturl)
    # set soup to the page of the url
    soup = BeautifulSoup(page.text, 'html')
    # find the table of airfoils
    options = soup.find('table', class_='afSearchResult')
    # find where the right area in the table is
    options = options.find_all('td', class_="cell3")
    # navigate through all of the airfoils on the table
    for i in range(0, len(options), 1):
        # The partial url of the selected airfoil
        suburl = options[i].find_all('a')[0].get("href")
        # print(suburl)
        # Full url of selected airfoil
        foilurl = "http://airfoiltools.com" + suburl
        # print(foilurl)

        # configure page for foil
        foilpage = requests.get(foilurl)
        foilsoup = BeautifulSoup(foilpage.text, 'html')
        foiltable = foilsoup.find('table', class_='polar')
        # selects the reynolds 200000 and Ncrit 9 option

        try:
            foilrow = foiltable.find_all('tr', class_="row0")[2]
            # print(foilrow)
            # Finds the partial url for foil details
            foilcell = foilrow.find_all('td')[7].find('a').get("href")
            foildetailsurl = "http://airfoiltools.com" + foilcell
            # print(foildetailsurl)

            # set up details page
            detailspage = requests.get(foildetailsurl)
            detailsoup = BeautifulSoup(detailspage.text, 'html')
            # pulls the link to the details csv
            detaillink = "http://airfoiltools.com" + \
                         detailsoup.find('table', class_="details").find_all('tr')[1].find('td', class_="cell1").find_all(
                             'a')[3].get("href")
            # print(detaillink)

            # configures csv link (still in html format, but will convert to csv
            downloadpage = requests.get(detaillink)
            downloadsoup = BeautifulSoup(downloadpage.text, 'html')
            # converts soup into text which is formatted as csv
            downloadsoupstr = str(downloadsoup)
            # print(downloadsoupstr)

            # This code goes through the data for the selected airfoil and finds the url, name, and data for alpha = 0 (sometimes not there so use 0.25 instead), 3, 5, 7.5, 10

            # Split the text into lines
            lines = downloadsoupstr.strip().split('\n')

            for line in lines:
                if line.startswith("Url"):
                    url = line

            for line in lines:
                if line.startswith("Airfoil"):
                    airfoil = line

            for line in lines:
                if line.startswith("0.00"):
                    cl0 = line.split(',')[1]
                    cd0 = line.split(',')[2]
                    ld0 = str(float(cl0) / float(cd0))
                    break
                elif line.startswith("0.250"):
                    cl0 = line.split(',')[1]
                    cd0 = line.split(',')[2]
                    ld0 = str(float(cl0) / float(cd0))
                    break

            for line in lines:
                if line.startswith("3.00"):
                    cl3 = line.split(',')[1]
                    cd3 = line.split(',')[2]
                    ld3 = str(float(cl3) / float(cd3))
                    break

            for line in lines:
                if line.startswith("5.00"):
                    cl5 = line.split(',')[1]
                    cd5 = line.split(',')[2]
                    ld5 = str(float(cl5) / float(cd5))
                    break

            for line in lines:
                if line.startswith("7.50"):
                    cl75 = line.split(',')[1]
                    cd75 = line.split(',')[2]
                    ld75 = str(float(cl75) / float(cd75))
                    break

            for line in lines:
                if line.startswith("10.00"):
                    cl10 = line.split(',')[1]
                    cd10 = line.split(',')[2]
                    ld10 = str(float(cl10) / float(cd10))
                    break

            max_Cl = -1.0 * math.inf
            for row in range(11, len(lines)-1, 1):
                rowCl = lines[row].split(',')[1]
                if float(rowCl) > max_Cl:
                    max_Cl = float(rowCl)


            # prints the data in readable way
            #print(str(pageNum) + "\n" + airfoil + "\n" + "L/D- 0 Deg Alpha- " + ld0 + "\n" + "L/D- 3 Deg Alpha- " + ld3 + "\n" + "L/D- 5 Deg Alpha- " + ld5 + "\n" + "L/D- 7.5 Deg Alpha- " + ld75 + "\n" + "L/D- 10 Deg Alpha- " + ld10 + "\n" + url + "\n\n ")
            # Write data to the CSV file
            data_to_write = [airfoil, url[4:], cl0, cd0, ld0, cl3, cd3, ld3, cl5, cd5, ld5, cl75, cd75, ld75, cl10, cd10, ld10, max_Cl]
            with open(file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(data_to_write)
        except AttributeError:
            print(
                "Error: Could not find the table rows. Check if the HTML structure has changed or if the data is available.\n"+foilurl)
            # Handle the error gracefully, perhaps by logging or notifying the user.
        except IndexError:
            print("Error: Index out of range. Make sure there are enough elements in the list before accessing them.\n"+foilurl)
            # Handle the IndexError gracefully, perhaps by logging or notifying the user.


    pageNum = pageNum + 1
    print(pageNum)
