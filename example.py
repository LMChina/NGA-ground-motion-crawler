from nga_ground_motion_download import NGAGroundMotionDownload

# Enter your email and password for NGA West2 website
database = 'nga sub'
if database == 'nga west2':
    email = 'limao0632@163.com'
    password = 'limao123'
    flatfile_name = 'Updated_NGA_West2_Flatfile_RotD50_d005_public_version.xlsx'
    rsn = [1]
else:
    email = 'limao0632@gmail.com'
    password = 'qwer1234'
    flatfile_name = 'NGAsubDb_PSA_RotD50_050_public_R230104.csv'
    rsn = [1000001]


# Choose the browser type to use for downloading the ground motions. Options are 'chrome' and 'edge'
browser_type = 'edge'

# Choose the ground motions to download. Options are 'horizontal 1', 'horizontal 2','vertical'
gm_directions = ['horizontal 1']

# Run the download script
NGAGroundMotionDownload.run_download_script(email, password, flatfile_name, browser_type, gm_directions, rsn, database)

