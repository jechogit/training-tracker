# Training Tracker App

A Streamlit application that helps you track and optimize your training routine. The app provides personalized workout recommendations based on your training history and ensures proper rest periods between workouts.

## Features

- Determines whether today is a training or rest day
- Recommends specific exercises based on your training history
- Calculates optimal repetitions per set using your performance data
- Displays a heatmap visualization of your training history
- Stores training data in Google Sheets

## Deployment on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your forked repository
5. Set the following secrets in Streamlit Cloud:
   - `GOOGLE_SHEETS_CREDENTIALS`: The entire content of your Google Sheets credentials JSON file
   - `SPREADSHEET_ID`: Your Google Sheets spreadsheet ID
6. Click "Deploy"

## Local Development

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.streamlit/secrets.toml` file with your credentials:
   ```toml
   GOOGLE_SHEETS_CREDENTIALS = '''
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "your-private-key-id",
     "private_key": "your-private-key",
     "client_email": "your-service-account-email",
     "client_id": "your-client-id",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "your-cert-url"
   }
   '''
   SPREADSHEET_ID = "your-spreadsheet-id"
   ```

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