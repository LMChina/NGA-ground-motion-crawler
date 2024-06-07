"""
-*- coding: utf-8 -*-

This is the class that includes the NGA West 2 ground motion download script.
The script will download the specified ground motion files from the NGA West 2 database: https://ngawest2.berkeley.edu/
The flatfile can be downloaded from the NGA West 2 website: https://peer.berkeley.edu/research/data-sciences/databases

Author: Mao Li
PhD student at University of Alberta, Canada
Date: 2024-05-09
"""

# Import necessary libraries
import os
import pandas as pd
import zipfile
import re
import numpy as np
import time
from selenium.webdriver import Edge, EdgeOptions, Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException


class NGAGroundMotionDownload:
    def __init__(self, account: str, password: str, flatfile_name: str, browser_type: str, gm_directions: list,
                 record_sequence_numbers: list, database_name: str):
        """
        :param account: NGA account email
        :param password: NGA account password
        :param flatfile_name: name of the flatfile of ground motion flatfile
        :param browser_type: type of browser to use, either 'edge' or 'chrome'
        :param gm_directions: list of ground motion directions to download, either 'horizontal1', 'horizontal2', or
        'vertical'
        :param record_sequence_numbers: list of record sequence numbers to download
        :param database_name: name of the database to download from, either 'NGA West2' or 'NGA Sub'
        """
        self.account = account
        self.password = password
        self.flatfile_name = flatfile_name
        self.browser_type = browser_type
        self.gm_directions = gm_directions
        self.current_path = os.getcwd()
        self.record_sequence_numbers = record_sequence_numbers

        if database_name.lower() not in ['nga west2', 'nga sub']:
            raise ValueError("Invalid database name. Please choose from 'NGA West2' or 'NGA Sub'.")
        else:
            self.database_name = database_name.lower()

    def get_ground_motion_info(self):
        """
        Read data from the flatfile and extract the record sequence numbers and file names for the specified ground
        motion directions.
        :return: a tuple of record sequence numbers and file names for the specified ground motion directions.
        """
        # check if flatfile exists
        if not os.path.isfile(self.flatfile_name):
            raise FileNotFoundError("Flatfile not found.")
        # read data
        RSNs = self.record_sequence_numbers
        if self.database_name == 'nga west2':
            df = pd.read_excel(self.flatfile_name)
        else:
            df = pd.read_csv(self.flatfile_name)

        # extract the acceleration file names
        acc_file_names = []
        if self.database_name == 'nga west2':
            rsn_head = 'Record Sequence Number'
            acc_head_1 = 'File Name (Horizontal 1)'
            acc_head_2 = 'File Name (Horizontal 2)'
            acc_head_v = 'File Name (Vertical)'
        else:
            rsn_head = 'NGAsubRSN'
            acc_head_1 = 'accFilePathH1'
            acc_head_2 = 'accFilePathH2'
            acc_head_v = 'accFilePathV'

        for rsn in RSNs:
            for direction in self.gm_directions:
                if direction == 'horizontal 1':
                    acc_file_name_base = df.loc[df[rsn_head] == rsn, acc_head_1].values[0]
                elif direction == 'horizontal 2':
                    acc_file_name_base = df.loc[df[rsn_head] == rsn, acc_head_2].values[0]
                elif direction == 'vertical':
                    acc_file_name_base = df.loc[df[rsn_head] == rsn, acc_head_v].values[0]
                else:
                    raise ValueError(
                        "Invalid direction. Please choose from 'horizontal1', 'horizontal2', or 'vertical'.")

                if self.database_name == 'nga west2':
                    acc_file_name = 'RSN' + str(rsn) + '_' + acc_file_name_base.replace('\\', '_')
                else:
                    file_name_part = os.path.basename(acc_file_name_base)
                    acc_file_name = rsn_head + str(rsn) + '_' + file_name_part

                acc_file_names.append(acc_file_name)

        return acc_file_names

    def download_ground_motion_file(self):
        if self.browser_type == 'edge':
            # Set up Edge browser
            options = EdgeOptions()
            prefs = {'download.default_directory': self.current_path}
            options.experimental_options["prefs"] = prefs
            options.add_experimental_option('detach', True)
            browser = Edge(options=options)
        elif self.browser_type == 'chrome':
            # Set up Chrome browser
            options = ChromeOptions()
            prefs = {'download.default_directory': self.current_path}
            options.add_experimental_option('prefs', prefs)
            browser = Chrome(options=options)
        else:
            raise ValueError("Unsupported browser type")

        # Open database website
        if self.database_name == 'nga west2':
            url = 'https://ngawest2.berkeley.edu/users/sign_in?unauthenticated=true'
        else:
            url = "http://ec2-35-167-122-9.us-west-2.compute.amazonaws.com/users/sign_in"

        browser.get(url)

        # wait for the page to load
        browser.implicitly_wait(100)

        if self.database_name == 'nga west2':
            # Login
            username_box = browser.find_element(By.NAME, "user[email]")
            password_box = browser.find_element(By.NAME, "user[password]")

            username_box.send_keys(self.account)
            password_box.send_keys(self.password)
            browser.find_element(By.ID, 'user_submit').click()

            # Check for login error
            try:
                error_message = browser.find_element(By.CSS_SELECTOR, "p.alert")
                if error_message.text == "Invalid email or password.":
                    raise ValueError("Invalid email or password.")
            except NoSuchElementException:
                pass  # No error message found, proceed with the rest of the code

            # Enter NGA West 2 Database
            browser.find_element(By.XPATH, "/html/body/div/div[8]/div/table[1]/tbody/tr[1]/td[2]/a/img").click()

            # Select Spectrum Model
            spectrum_model = browser.find_element(By.NAME, "spectra[NGAInputData_NGAModelSelection]")
            # No scaling = 88, PEER NGA-West2 Spectrum = 1, User Defined Spectrum = 0; ASCE Code Spectrum = 99
            Select(spectrum_model).select_by_value('88')
            browser.find_element(By.CSS_SELECTOR, "button[onclick='OnSubmit();']").click()

            # Enter record series number
            rsn = browser.find_element(By.ID, "search_search_nga_number")
            rsn.clear()
            RSNs_str = ','.join(map(str, self.record_sequence_numbers))
            rsn.send_keys(RSNs_str)
            search_button_css = "button[onclick='uncheck_plot_selected();reset_selectedResult();OnSubmit();']"
            browser.find_element(By.CSS_SELECTOR, search_button_css).click()

            # Select the spectral ordinate
            spectral_ordinate = browser.find_element(By.NAME, "search[SRkey]")
            select = Select(spectral_ordinate)
            # SRSS = 1, RotD100 = 2, RotD50 = 3, GeoMean = 4, H1 = 5, H2 = 6, V=7
            select.select_by_value('3')  # Select RotD50

            # download ground motion file
            download_button_css = "button[onclick='getSelectedResult(true)']"
            browser.find_element(By.CSS_SELECTOR, download_button_css).click()

            # accept the warning message
            browser.switch_to.alert.accept()
            browser.switch_to.alert.accept()

        else:
            # enter account information and login
            username_box = browser.find_element(By.NAME, "user[email]")
            password_box = browser.find_element(By.NAME, "user[password]")

            username_box.send_keys(self.account)
            password_box.send_keys(self.password)
            browser.find_element(By.NAME, 'commit').click()

            # Enter portal
            browser.find_element(By.XPATH, '/html/body/div/ul/li[1]/h3/a').click()

            # choose Target spectrum method
            # No Target Spectrum = 88,
            # NGA-Subduction Ground-Motion Model Spectrum = 1,
            # User Defined Spectrum = 0,
            # ASCE Code Spectrum = 99
            Select(browser.find_element(By.NAME, 'ngasubduction[NGAModelSelection]')).select_by_value('88')

            # Start project
            browser.find_element(By.NAME, 'commit').click()

            # enter record series number
            rsn_box = browser.find_element(By.ID, 'ngasubduction_search_rsn_list')
            rsn_box.clear()
            rsn_box.send_keys(','.join(map(str, self.record_sequence_numbers)))

            # choose spectral ordinate
            # RotD50 = RotD50,
            # RotD100 = RotD100,
            # H1 = H1,
            # H2 = H2,
            # V = V
            sr_id = 'ngasubduction_search_spectrumresultant'
            Select(browser.find_element(By.ID, sr_id)).select_by_value('RotD50')

            # download ground motion file
            browser.find_element(By.NAME, 'user_submitAction').click()

            # Download Unscaled Time Series & Metadata (Target & Search)
            x_path = '//*[@id="chart_Div_DownloadButtons"]/fieldset/input[2]'
            browser.find_element(By.XPATH, x_path).click()

            # download button
            browser.find_element(By.LINK_TEXT, '>> Click here to Agree & Download <<').click()

        # wait for the download to complete
        time.sleep(8)

        # close the browser
        browser.quit()

    def find_latest_downloaded_file(self):
        # find the latest downloaded zip file

        downloaded_files = os.listdir(self.current_path)
        downloaded_files = [f for f in downloaded_files if f.endswith('.zip')]
        try:
            latest_file = max(downloaded_files, key=os.path.getctime)
        except ValueError:
            raise ValueError("No downloaded files found, please check if the download was successful, if downloading is"
                             " not finished, please increase the sleep time in the download_ground_motion_file "
                             "function (time.sleep(8)).")
        return latest_file

    def unzip_files(self, latest_file):
        # check if the downloaded file is a zip file
        if not latest_file.endswith('.zip'):
            raise ValueError("Downloaded file is not a zip file.")

        # unzip file to a folder with the same name as the zip file
        zip_file_path = os.path.join(self.current_path, latest_file)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.splitext(zip_file_path)[0])

        # rename the folder as "raw ground motion data"
        os.rename(os.path.splitext(zip_file_path)[0], 'raw ground motion data')

    def organize_acceleration_data(self, acc_file_names):
        """
        This function reads the acceleration data from the downloaded records and organizes it into a DataFrame.
        The acceleration data is stored in a list of arrays, where each array contains the acceleration data for a single record
        series. The first element of each array is the dt, and the second element is the number of points. The remaining
        elements are the acceleration values. The function pads shorter arrays with NaN to match the longest array.
        :param acc_file_names: File names of the downloaded acceleration data files
        :return: acceleration data DataFrame: The first element of each array is the dt, and the second element is the
        number of points. The remaining elements are the acceleration values. The function pads shorter arrays with NaN to
        match the longest array.
        """

        all_acc_data = []
        max_length = 0  # Variable to store the maximum length of the arrays

        for file_name in acc_file_names:

            file_path = os.path.join(self.current_path, 'raw ground motion data', file_name)

            with open(file_path, 'r') as f:
                for _ in range(3):
                    next(f)
                line = next(f)
                npts_match = re.search(r"NPTS=\s*(\d+)", line)
                dt_match = re.search(r"DT=\s*(\d*\.\d+)", line)

                if npts_match and dt_match:
                    npts = int(npts_match.group(1))
                    dt = float(dt_match.group(1))
                else:
                    print(f"File {file_name} has incorrect format. Skipping file.")
                    continue  # Skip files with incorrect formats

                acc_data = []
                total_acc_lines = (npts + 4) // 5
                for _ in range(total_acc_lines):
                    line = f.readline()
                    values = line.strip().split()
                    acc_data.extend([float(v) for v in values])

                acc_data.insert(0, dt)  # Insert dt at the beginning
                acc_data.insert(0, int(npts))  # Insert npts at the beginning
                all_acc_data.append(acc_data)

                if len(acc_data) > max_length:
                    max_length = len(acc_data)  # Update the maximum length found

        # Pad shorter arrays with NaN to match the longest array
        all_acc_data = [data + [np.nan] * (max_length - len(data)) for data in all_acc_data]

        # Create DataFrame
        acc_df = pd.DataFrame({
            acc_file_names: data for acc_file_names, data in zip(acc_file_names, all_acc_data)
        })

        return acc_df

    @staticmethod
    def run_download_script(email: str, password: str, flatfile_name: str, browser_type: str, gm_directions: list,
                            record_sequence_numbers: list, database_name: str):
        """
        This function runs the NGA West 2 ground motion download script.
        :param record_sequence_numbers: record sequence numbers of the ground motion records to download
        :param email: NGA West 2 account email
        :param password: NGA West 2 account password
        :param flatfile_name: name of the flatfile of NGA West 2 ground motion data
        :param browser_type: type of browser to use, either 'edge' or 'chrome'
        :param gm_directions: list of ground motion directions to download, either 'horizontal1', 'horizontal2', or
       'vertical'
        :param database_name: name of the record database flatfile, either 'nga west2' or 'nga sub'
        """

        downloader = NGAGroundMotionDownload(email, password, flatfile_name, browser_type, gm_directions,
                                             record_sequence_numbers, database_name)
        acc_file_names = downloader.get_ground_motion_info()
        downloader.download_ground_motion_file()
        latest_file = downloader.find_latest_downloaded_file()
        downloader.unzip_files(latest_file)
        acc_df = downloader.organize_acceleration_data(acc_file_names)
        acc_df.to_csv('acceleration_data.csv', index=False)  # Save acceleration data to a CSV file
