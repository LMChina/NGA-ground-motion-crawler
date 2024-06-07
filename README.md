# NGA-ground-motion-crawler

This Python script automates the process of downloading ground motion data files from the NGA West 2 database (https://ngawest2.berkeley.edu/), and NGA Subduction database (https://www.risksciences.ucla.edu/nhr3/nga-subduction)

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

1. Obtain a valid NGA West2 or NGA Subduction account and its credentials (email and password).
2. Download the NGA West2 and NGA Subduction flatfile (https://peer.berkeley.edu/research/data-sciences/databases), and (https://www.risksciences.ucla.edu/nhr3/nga-subduction/psa-tables-r230104) respectively. An example of the flatfile also can be downloaded from https://drive.google.com/drive/folders/1AIu7K_h1-9vWdtB2-W-BNP1qelUqFGmb?usp=sharing
3. Run the example script with the necessary arguments or in your IDE:
4. The script will automate the download process, extract the acceleration data, and save it as a CSV file named `acceleration_data.csv` in the current working directory.

## Example
Here's an example of how to use the script:

```python
from nga_ground_motion_download import NGAGroundMotionDownload

# Enter your email and password for NGA West2 website
database = 'nga sub'
if database == 'nga west2':
    email = 'your_email@xxx.com'
    password = 'your_password'
    flatfile_name = 'Updated_NGA_West2_Flatfile_RotD50_d005_public_version.xlsx'
    rsn = [1]
else:
    email = 'your_email@xxx.com'
    password = 'your_password'
    flatfile_name = 'NGAsubDb_PSA_RotD50_050_public_R230104.csv'
    rsn = [1000001]

# Choose the browser type to use for downloading the ground motions. Options are 'chrome' and 'edge'
browser_type = 'edge'

# Choose the ground motions to download. Options are 'horizontal 1', 'horizontal 2','vertical'
gm_directions = ['horizontal 1']
# gm_directions = ['horizontal 1', 'horizontal 2','vertical']

# Run the download script
NGAGroundMotionDownload.run_download_script(email, password, flatfile_name, browser_type, gm_directions, rsn, database)
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

Special thanks to the Pacific Earthquake Engineering Research Center (PEER) at the University of California, Berkeley, for developing and maintaining the NGA West 2 database, and Natural Hazards Risk and Resiliency Research Center (NHR3) for developing and maintaining the NGA Subduction database. Also, thanks to the WeChat public account "非解构" for providing basic knowledge on this topic.
