# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--search-key", type=str)
parser.add_argument("--number-of-images", type=int)
parser.add_argument("--number-of-workers", type=int)

args = parser.parse_args()

def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path, image_path, search_key, number_of_images, headless, min_resolution, max_resolution)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls)

    #Release resources
    del image_scraper

if __name__ == "__main__":
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys = [args.search_key]

    #Parameters
    number_of_images = args.number_of_images              # Desired number of images
    headless = True                    # True = No Chrome GUI
    min_resolution = (500, 500)            # Minimum desired image resolution
    max_resolution = (4096, 4096)      # Maximum desired image resolution
    max_missed = 100                    # Max number of failed images before exit
    number_of_workers = args.number_of_workers              # Number of "workers" used

    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)
