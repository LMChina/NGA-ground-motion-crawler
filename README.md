# NGAWest2-ground-motion-crawler

This Python script automates the process of downloading ground motion data files from the NGA West 2 database (https://ngawest2.berkeley.edu/), developed by the Pacific Earthquake Engineering Research Center (PEER) at the University of California, Berkeley.

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository or download the script file.
2. Install the required Python libraries using the `requirements.txt` file:

```
pip install -r requirements.txt
```

3. Download the appropriate WebDriver for your browser (Chrome or Edge) and ensure it's in your system's PATH.

## Usage

1. Obtain a valid NGA West 2 account and its credentials (email and password).
2. Download the NGA West 2 flatfile containing ground motion data information from the PEER website (https://peer.berkeley.edu/research/data-sciences/databases).
3. Run the script with the necessary arguments or in your IDE:

```
python nga_west2_download.py --email your_email@example.com --password your_password --flatfile flatfile.xlsx --browser edge --directions horizontal1 horizontal2 vertical
```

Replace the placeholders with your actual email, password, flatfile name, browser type (edge or chrome), and desired ground motion directions (horizontal1, horizontal2, vertical).

4. The script will automate the download process, extract the acceleration data, and save it as a CSV file named `acceleration_data.csv` in the current working directory.

## Example

Here's an example of how to use the script:

```python
from nga_west2_ground_motion_download import NGAWest2GroundMotionDownload

# Enter your email and password for NGA West2 website
email = 'your_email_address@provider.com'
password = 'your_password'

# The flatfile must be filtered to only include the desired ground motions which less than the maximum records
# limitation: The current limit is set at approximately 200 records every two weeks, 400 every month
flatfile_name = 'Updated_NGA_West2_Flatfile_RotD50_d005_public_version.xlsx'

# Choose the browser type to use for downloading the ground motions. Options are 'chrome' and 'edge'
browser_type = 'edge'

# Choose the ground motions to download. Options are 'horizontal 1', 'horizontal 2','vertical'
gm_directions = ['horizontal 1', 'horizontal 2', 'vertical']

# Run the download script
NGAWest2GroundMotionDownload.run_download_script(email, password, flatfile_name, browser_type, gm_directions)
```

This example demonstrates how to create an instance of the `NGAWest2GroundMotionDownload` class and run the `run_download_script` method to initiate the download process.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This script utilizes the following libraries:

- pandas
- selenium
- numpy

Special thanks to the Pacific Earthquake Engineering Research Center (PEER) at the University of California, Berkeley, for developing and maintaining the NGA West 2 database.
