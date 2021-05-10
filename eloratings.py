#!/usr/bin/env python
# coding: utf-8

import json
import time
import logging
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

HEADER = ["Rank Local", "Rank Global", 
          "Team", "Rating", 
          "Average Rank", "Average Rating", 
          "1 Year Change Rank", "1 Year Change Rating", 
          "Matches Total", "Matches Home", "Matches Away", "Matches Neutral", 
          "Matches Wins", "Matches Losses", "Matches Draws", 
          "Goals For", "Goals Against"]
YEARS = ["2000", "2004", "2008", "2012", "2016", "2021"]
CURRENT = "2021"
TOURNAMENTS = ["European_Championship"]
SUFFIXES = ["start"]


def process_page(page_name):
    """process one page of ratings
    Args:
        browser: Instantiated browser session
        page_name:  Name of page on website
    Returns:
        (saves data to json file)
    """
    logging.info("Processing {0}".format(page_name))

    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)
    logging.debug(type(browser))
    try:
        browser.get("http://eloratings.net/{0}".format(page_name))
        time.sleep(10)

        main = browser.find_element_by_id("maintable_{0}".format(page_name))

        body = main.find_element_by_class_name("grid-canvas")

        rows = body.find_elements_by_class_name("ui-widget-content")
        logging.debug("input rows: {0}".format(len(rows)))

        rows[0].find_elements_by_class_name("slick-cell")[0].text

        data = {}
        data["Team"] = []
        for row in rows:
            rec = {}
            for i, title in enumerate(HEADER):
                rec[title] = row.find_elements_by_class_name("slick-cell")[i].text
            data["Team"].append(rec)

        logging.debug("output rows: {0}".format(len(data["Team"])))

        with open('{0}.json'.format(page_name), 'w') as outfile:
            json.dump(data, outfile)
    
    except Exception as e:
        logging.error("Processing failed on {0}".format(page_name))
        logging.debug(e)
        
    finally:
        browser.close()
        browser.quit()

    return


def scrape_elo():
    """run scraper on website
    Args:
        None
    Returns:
        None
    """
    logging.info("Starting scrape of website")

    for y in YEARS:
        for t in TOURNAMENTS:
            for s in SUFFIXES:
                if y == CURRENT:
                    page = "{0}_{1}".format(y, t)
                else:
                    page = "{0}_{1}_{2}".format(y, t, s)

                logging.debug(page)
                process_page(page)

    return


if __name__ == '__main__':
    scrape_elo()
