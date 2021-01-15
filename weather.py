import csv
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

dates_to_evaluate = True
count = 0

# while the is dates with no data, the loop continue
# if after 3 try there still is no data the loop end (some date are not available on the web site)
while dates_to_evaluate and count <= 3:

    # Instantiate an Options object
    # and add the “ — headless” argument
    opts = Options()
    opts.add_argument(" — headless")
    # Set the location of the webdriver
    chrome_driver = "./chromedriver"
    # Instantiate a webdriver
    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

    # try to open reddit and twitter csv to take the dates
    dates = []
    try:
        reddit = pd.read_csv("reddit_AustinFC.csv")
        dates_reddit = reddit["created date"].tolist()
        for date in dates_reddit:
            dates.append(date)
    except:
        print("no reddit csv found")
    try:
        twitter = pd.read_csv("twitter_AustinFC.csv")
        dates_twitter = twitter["date"].tolist()
        for date in dates_twitter:
            array = date.split("-")
            date = f"{array[2]}/{array[1]}/{array[0]}"
            dates.append(date)
    except:
        print("no twitter csv found")

    # delete dates that appear several times
    dates = list(dict.fromkeys(dates))

    # open weather.csv to check already recorded weather data
    try:
        with open('weather_Austin.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] in dates:
                    dates.remove(row[0])
    except:
        print('No existing weather.csv')

    dates_not_recorded = []
    # initiate data storage
    high_temps = []
    low_temps = []
    day_average_temps = []
    precipitations = []
    max_wind_speeds = []

    for date in dates:
        # extraction of the date parameters
        array = date.split("/")
        year = array[2]
        month = str(int(array[1]))  # convert to int then string to remove potentially useless 0
        day = str(int(array[0]))
        # write the url with the year-month-day parameters
        url = "https://www.wunderground.com/history/daily/us/tx/austin/KAUS/date/" + str(year) + "-" + str(
            month) + "-" + str(day)
        # Load the HTML page
        driver.get(url)

        # Put the page source into a variable and create a BS object from it
        soup_file = driver.page_source
        soup = BeautifulSoup(soup_file, 'html.parser')
        result = []

        # wait of the response by the server
        wait = WebDriverWait(driver, 15)
        wait.until(presence_of_element_located((By.CLASS_NAME, "summary-table")))

        # Search html inside <div> with class:"summary-table"
        for elt in soup.find_all("div", attrs={"class": "summary-table"}):
            # Search all <th> inside <tr> in a list
            for th in elt.find_all(["tr", "th"]):
                # Search of td in th
                for td in th.find_all(["td"]):
                    result.append(td.text.strip())

        try:
            # format the result to select only useful parameters and convert it into good units
            value = (int(result[4]) - 32) * 5 / 9  # converting Farenheit to Celcius
            high_temps.append(float("{:.2f}".format(value)))
            value = (int(result[7]) - 32) * 5 / 9  # converting Farenheit to Celcius
            low_temps.append(float("{:.2f}".format(value)))
            value = (float(result[10]) - 32) * 5 / 9  # converting Farenheit to Celcius
            day_average_temps.append(float("{:.2f}".format(value)))
            value = (float(result[17])) * 25.4  # converting inches to mm
            precipitations.append(float("{:.2f}".format(value)))
            value = (float(result[40])) * 1.609  # converting mph to kmh
            max_wind_speeds.append(float("{:.2f}".format(value)))
        except:
            # If data are not loaded, the corresponding date is added to the dates_ot_recorded list
            dates_not_recorded.append(date)
            print(f"{date} not recorded")

    # close the opened webpages
    driver.quit()

    # Removes the not recorded dates from the dates list
    for date in dates_not_recorded:
        dates.remove(date)
    print(dates)
    # pandas dataframe
    weather_data = pd.DataFrame({
        'created date': dates,
        'Highest Temperature': high_temps,
        'Lowest Temperature': low_temps,
        'Day Average Temperature': day_average_temps,
        'Precipitation': precipitations,
        'Max Wind Speed': max_wind_speeds
    })

    # check if weather.csv exists to write or not the headers
    if os.path.exists('weather_Austin.csv'):
        weather_data.to_csv('weather_Austin.csv', mode='a', header=False, index=False)
    else:
        weather_data.to_csv('weather_Austin.csv', mode='a', header=True, index=False)

    # increase of the count
    count += 1
    # if all data loaded, the while loop stop
    if len(dates_not_recorded) == 0:
        dates_to_evaluate = False
