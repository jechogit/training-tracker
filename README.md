# Training Tracker App

A Streamlit application that helps you track and optimize your training routine. The app provides personalized workout recommendations based on your training history and ensures proper rest periods between workouts.

## Features

- Determines whether today is a training or rest day
- Recommends specific exercises based on your training history
- Calculates optimal repetitions per set using your performance data
- Displays a heatmap visualization of your training history
- Stores training data in Google Sheets

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Sheets integration:

   ### Step 1: Create a Google Cloud Project
   1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
   2. Click on the project dropdown at the top of the page
   3. Click "New Project"
   4. Enter a name for your project and click "Create"

   ### Step 2: Enable the Google Sheets API
   1. In your new project, go to "APIs & Services" > "Library"
   2. Search for "Google Sheets API"
   3. Click on it and then click "Enable"

   ### Step 3: Create a Service Account
   1. Go to "IAM & Admin" > "Service Accounts"
   2. Click "Create Service Account"
   3. Enter a name for the service account (e.g., "training-tracker")
   4. Click "Create and Continue"
   5. For Role, select "Project" > "Editor"
   6. Click "Continue" and then "Done"

   ### Step 4: Create and Download Credentials
   1. Find your new service account in the list
   2. Click on the three dots menu (⋮) on the right
   3. Select "Manage keys"
   4. Click "Add Key" > "Create new key"
   5. Choose "JSON" format
   6. Click "Create" - this will download a JSON file

   ### Step 5: Set Up the Credentials File
   1. Rename the downloaded JSON file to `credentials.json`
   2. Place it in the root directory of this project
   3. Make sure the file is listed in `.gitignore` to prevent accidental commits

   ### Step 6: Create and Share a Google Sheet
   1. Go to [Google Sheets](https://sheets.google.com)
   2. Create a new spreadsheet
   3. Click the "Share" button in the top right
   4. Add the service account email (found in the `client_email` field of your credentials.json)
   5. Give it "Editor" access
   6. Copy the spreadsheet ID from the URL:
      - Open your Google Sheet
      - Look at the URL in your browser
      - The URL will look like: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
      - Copy the long string of characters between `/d/` and `/edit`
      - This is your spreadsheet ID
   7. Open `app.py` and replace `YOUR_SPREADSHEET_ID` with the ID you copied

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the app in your web browser
2. The app will automatically:
   - Determine if today is a training or rest day
   - Recommend an exercise based on your training history
   - Calculate the optimal number of repetitions
   - Show your training history in a heatmap

3. After completing your workout, you can log your performance in the app

## Training Logic

- The app ensures at least 72 hours of rest between workouts for the same muscle group
- Daily sets and reps are calculated at 80% of your estimated max capacity
- Training is structured in 7-day cycles
- The app uses a moving average to estimate your max capacity
- If no history exists for an exercise, a baseline training day is assigned

## Security Notes

- Never commit the `credentials.json` file to version control
- Keep your private key secure and never share it
- The `.gitignore` file is set up to exclude sensitive files
- Make sure to restrict access to your Google Sheet appropriately

## Contributing

Feel free to submit issues and enhancement requests! 