import pandas as pd

# 1. Load the email data
# We'll load just the first 5000 rows to keep it fast
df = pd.read_csv('email.csv', nrows=5000)

# 2. Convert the 'date' column into something Python understands
df['date'] = pd.to_datetime(df['date'])

# 3. Extract the 'hour' the email was sent (0 to 23)
df['hour'] = df['date'].dt.hour

print("--- Data Check Successful ---")
print(f"Total rows loaded: {len(df)}")
print("\nFirst 5 rows of your email data:")
print(df[['date', 'user', 'to', 'hour']].head())

# 4. Count how many emails were sent late at night (e.g., between 11 PM and 5 AM)
late_emails = df[(df['hour'] >= 23) | (df['hour'] <= 5)]
print(f"\nNumber of potential after-hours emails found: {len(late_emails)}")