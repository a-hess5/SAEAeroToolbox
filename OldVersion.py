# First version of the Airfoil Scraping Script.
# This was replaced by AirfoilScrape.py

from bs4 import BeautifulSoup
import requests
import csv

file_path = "foil_data.csv"
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write header row (optional)
    header = ["Name", "Data Url", "L/D- 0 Deg Alpha- ", "L/D- 3 Deg Alpha- ", "L/D- 5 Deg Alpha- ", "L/D- 7.5 Deg Alpha- ", "L/D- 10 Deg Alpha- "]
    writer.writerow(header)

pageNum = 0

while (pageNum < 164):
    starturl = "http://airfoiltools.com/search/index?m%5BtextSearch%5D=&m%5BmaxCamber%5D=&m%5BminCamber%5D=&m%5BmaxThickness%5D=&m%5BminThickness%5D=&m%5Bgrp%5D=&m%5Bsort%5D=1&m%5Bpage%5D=" + str(pageNum) + "&m%5Bcount%5D=1638"
    page = requests.get(starturl)
    soup = BeautifulSoup(page.text, 'html.parser')
    options = soup.find('table', class_='afSearchResult')

    if options:
        options = options.find_all('td', class_="cell3")

        for i in range(0, len(options), 1):
            suburl = options[i].find_all('a')[0].get("href")
            foilurl = "http://airfoiltools.com" + suburl

            foilpage = requests.get(foilurl)
            foilsoup = BeautifulSoup(foilpage.text, 'html.parser')
            foiltable = foilsoup.find('table', class_='polar')

            if foiltable:
                foilrows = foiltable.find_all('tr', class_="row0")

                if len(foilrows) > 2:
                    foilrow = foilrows[2]
                    foilcell = foilrow.find_all('td')[7].find('a').get("href")
                    foildetailsurl = "http://airfoiltools.com" + foilcell

                    detailspage = requests.get(foildetailsurl)
                    detailsoup = BeautifulSoup(detailspage.text, 'html.parser')
                    details_table = detailsoup.find('table', class_="details")

                    if details_table:
                        detaillink = "http://airfoiltools.com" + details_table.find_all('tr')[1].find('td', class_="cell1").find_all(
                                     'a')[3].get("href")

                        downloadpage = requests.get(detaillink)
                        downloadsoup = BeautifulSoup(downloadpage.text, 'html.parser')
                        downloadsoupstr = str(downloadsoup)

                        lines = downloadsoupstr.strip().split('\n')

                        airfoil = ""
                        url = ""
                        ld0 = ld3 = ld5 = ld75 = ld10 = ""

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

                        data_to_write = [airfoil, url, ld0, ld3, ld5, ld75, ld10]

                        with open(file_path, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(data_to_write)

    pageNum = pageNum + 1
    print(pageNum)
