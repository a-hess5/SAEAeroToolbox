# Imports
##############################
import math
from bs4 import BeautifulSoup
import requests
import csv

# Create CSV File
##############################
file_path = "foil_data_new_pg81-90.csv"
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write header row (optional)
    header = ["Name", "Data Url", "Reynold's Number", "Alpha", "CL", "CD"]
    writer.writerow(header)


# Scrape Site for Airfoils
##############################

#Page number of airfoils
pageNum = 81

while (pageNum < 164):  # 164 pages as of 10/7/2024
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

# Select Airfoil Data Listing
##############################

        # selects the reynolds 50000 and Ncrit 9 option

        try:
            foilrow = foiltable.find_all('tr', class_="row0")[0]
            # print(foilrow)
            # Finds the partial url for foil details
            foilcell = foilrow.find_all('td')[7].find('a').get("href")
            foildetailsurl = "http://airfoiltools.com" + foilcell
            #print(foildetailsurl)

            # set up details page
            detailspage = requests.get(foildetailsurl)
            detailsoup = BeautifulSoup(detailspage.text, 'html')
            # pulls the link to the details csv
            detaillink = "http://airfoiltools.com" + \
                         detailsoup.find('table', class_="details").find_all('tr')[1].find('td', class_="cell1").find_all(
                             'a')[3].get("href")
            #print(detaillink)

            # configures csv link (still in html format, but will convert to csv
            downloadpage = requests.get(detaillink)
            downloadsoup = BeautifulSoup(downloadpage.text, 'html')
            # converts soup into text which is formatted as csv
            downloadsoupstr = str(downloadsoup)
            #print(downloadsoupstr)

            # This code goes through the data for the selected airfoil and finds the url, name, and data for alpha = 0 (sometimes not there so use 0.25 instead), 3, 5, 7.5, 10

            # Split the text into lines
            lines = downloadsoupstr.strip().split('\n')
            zeroIndex = -1 #Index of the first
            for line in lines:
                if line.startswith("Url"):
                    url = line

            for line in lines:
                if line.startswith("Airfoil"):
                    airfoil = line

            #Look for the zero degree alpha to know where to start getting data
            for line in range(len(lines)):
                if lines[line].startswith("0.00"):
                    zeroIndex = line
                    break
                # Sometimes there is no zero degree alpha in the spec sheet- this replaces it with the .25 degree alpha
                elif lines[line].startswith("0.250"):
                    zeroIndex = line
                    break

            alphaRow = zeroIndex #Start at the index of the zero alpha
            largestCL = -math.inf #Set the parameter for largest Cl
            dataRow = lines[alphaRow].split(',') #Define the first row of data and split it by commas

            while alphaRow < len(lines) and float(dataRow[1])>=largestCL: #Loop through the rows by alpha until the stall point, then stop
                largestCL = float(dataRow[1])
                data_to_write = [airfoil, url[4:], 50000, dataRow[0], dataRow[1], dataRow[2]]
                with open(file_path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(data_to_write)
                alphaRow+=1
                dataRow = lines[alphaRow].split(',')

        except AttributeError:
            print(
                "Error: Could not find the table rows. Check if the HTML structure has changed or if the data is available.\n"+foilurl)
            # Handle the error gracefully, perhaps by logging or notifying the user.
        except IndexError:
            print("Error: Index out of range. Make sure there are enough elements in the list before accessing them.\n"+foilurl)
            # Handle the IndexError gracefully, perhaps by logging or notifying the user.




        # selects the reynolds 100000 and Ncrit 9 option

        try:
            foilrow = foiltable.find_all('tr', class_="row1")[0]
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
                         detailsoup.find('table', class_="details").find_all('tr')[1].find('td',
                                                                                           class_="cell1").find_all(
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
            zeroIndex = -1  # Index of the first
            for line in lines:
                if line.startswith("Url"):
                    url = line

            for line in lines:
                if line.startswith("Airfoil"):
                    airfoil = line

            # Look for the zero degree alpha to know where to start getting data
            for line in range(len(lines)):
                if lines[line].startswith("0.00"):
                    zeroIndex = line
                    break
                # Sometimes there is no zero degree alpha in the spec sheet- this replaces it with the .25 degree alpha
                elif lines[line].startswith("0.250"):
                    zeroIndex = line
                    break

            alphaRow = zeroIndex  # Start at the index of the zero alpha
            largestCL = -math.inf  # Set the parameter for largest Cl
            dataRow = lines[alphaRow].split(',')  # Define the first row of data and split it by commas

            while alphaRow < len(lines) and float(
                    dataRow[1]) >= largestCL:  # Loop through the rows by alpha until the stall point, then stop
                largestCL = float(dataRow[1])
                data_to_write = [airfoil, url[4:], 100000, dataRow[0], dataRow[1], dataRow[2]]
                with open(file_path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(data_to_write)
                alphaRow += 1
                dataRow = lines[alphaRow].split(',')

        except AttributeError:
            print(
                "Error: Could not find the table rows. Check if the HTML structure has changed or if the data is available.\n"+foilurl)
            # Handle the error gracefully, perhaps by logging or notifying the user.
        except IndexError:
            print("Error: Index out of range. Make sure there are enough elements in the list before accessing them.\n"+foilurl)
            # Handle the IndexError gracefully, perhaps by logging or notifying the user.



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
                         detailsoup.find('table', class_="details").find_all('tr')[1].find('td',
                                                                                           class_="cell1").find_all(
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
            zeroIndex = -1  # Index of the first
            for line in lines:
                if line.startswith("Url"):
                    url = line

            for line in lines:
                if line.startswith("Airfoil"):
                    airfoil = line

            # Look for the zero degree alpha to know where to start getting data
            for line in range(len(lines)):
                if lines[line].startswith("0.00"):
                    zeroIndex = line
                    break
                # Sometimes there is no zero degree alpha in the spec sheet- this replaces it with the .25 degree alpha
                elif lines[line].startswith("0.250"):
                    zeroIndex = line
                    break

            alphaRow = zeroIndex  # Start at the index of the zero alpha
            largestCL = -math.inf  # Set the parameter for largest Cl
            dataRow = lines[alphaRow].split(',')  # Define the first row of data and split it by commas

            while alphaRow < len(lines) and float(
                    dataRow[1]) >= largestCL:  # Loop through the rows by alpha until the stall point, then stop
                largestCL = float(dataRow[1])
                data_to_write = [airfoil, url[4:], 200000, dataRow[0], dataRow[1], dataRow[2]]
                with open(file_path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(data_to_write)
                alphaRow += 1
                dataRow = lines[alphaRow].split(',')

        except AttributeError:
            print(
                "Error: Could not find the table rows. Check if the HTML structure has changed or if the data is available.\n" + foilurl)
            # Handle the error gracefully, perhaps by logging or notifying the user.
        except IndexError:
            print(
                "Error: Index out of range. Make sure there are enough elements in the list before accessing them.\n" + foilurl)
            # Handle the IndexError gracefully, perhaps by logging or notifying the user.


        # selects the reynolds 500000 and Ncrit 9 option

        try:
            foilrow = foiltable.find_all('tr', class_="row1")[2]
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
                         detailsoup.find('table', class_="details").find_all('tr')[1].find('td',
                                                                                           class_="cell1").find_all(
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
            zeroIndex = -1  # Index of the first
            for line in lines:
                if line.startswith("Url"):
                    url = line

            for line in lines:
                if line.startswith("Airfoil"):
                    airfoil = line

            # Look for the zero degree alpha to know where to start getting data
            for line in range(len(lines)):
                if lines[line].startswith("0.00"):
                    zeroIndex = line
                    break
                # Sometimes there is no zero degree alpha in the spec sheet- this replaces it with the .25 degree alpha
                elif lines[line].startswith("0.250"):
                    zeroIndex = line
                    break

            alphaRow = zeroIndex  # Start at the index of the zero alpha
            largestCL = -math.inf  # Set the parameter for largest Cl
            dataRow = lines[alphaRow].split(',')  # Define the first row of data and split it by commas

            while alphaRow < len(lines) and float(
                    dataRow[1]) >= largestCL:  # Loop through the rows by alpha until the stall point, then stop
                largestCL = float(dataRow[1])
                data_to_write = [airfoil, url[4:], 500000, dataRow[0], dataRow[1], dataRow[2]]
                with open(file_path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(data_to_write)
                alphaRow += 1
                dataRow = lines[alphaRow].split(',')

        except AttributeError:
            print(
                "Error: Could not find the table rows. Check if the HTML structure has changed or if the data is available.\n" + foilurl)
            # Handle the error gracefully, perhaps by logging or notifying the user.
        except IndexError:
            print(
                "Error: Index out of range. Make sure there are enough elements in the list before accessing them.\n" + foilurl)
            # Handle the IndexError gracefully, perhaps by logging or notifying the user.


    pageNum = pageNum + 1
    print(pageNum)