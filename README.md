# Sahara Readymade Store Management System

A Streamlit application for managing a readymade garment store.

## Features

- Category Management
- Product Management
- Customer Management
- Order Creation and Tracking
- Payment Status Tracking

## Setup Instructions

### Local Development

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=SaharaReadymade
   ```
4. Initialize the database using the provided SQL script:
   ```
   mysql -u root -p < db_schema.sql
   ```
5. (Optional) Load sample data:
   ```
   mysql -u root -p < sample_data.sql
   ```
6. Run the application:
   ```
   streamlit run sahara-readymade-app.py
   ```

### Deployment on Render

#### Step 1: Set up a MySQL Database

1. Choose a MySQL provider:
   - [PlanetScale](https://planetscale.com/) (Recommended - has free tier)
   - [Railway](https://railway.app/)
   - [AWS RDS](https://aws.amazon.com/rds/)
   - [Azure Database for MySQL](https://azure.microsoft.com/en-us/products/mysql/)

2. Create a MySQL database and note the connection details:
   - Host
   - Username
   - Password
   - Database name

#### Step 2: Deploy on Render

1. Create a Render account at https://render.com

2. From the Dashboard, click "New" and select "Web Service"

3. Connect your GitHub or GitLab repository

4. Configure the service:
   - **Name**: sahara-readymade
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run sahara-readymade-app.py`

5. Add Environment Variables:
   - `DB_HOST`: Your database host
   - `DB_USER`: Your database username
   - `DB_PASSWORD`: Your database password
   - `DB_NAME`: Your database name

6. Click "Create Web Service"

7. After deployment, access your app at the provided Render URL

#### Step 3: Initialize the Database

The application will automatically attempt to initialize the database on startup.

To load sample data, you can connect to your database service and run the `sample_data.sql` script.

## Troubleshooting

If you encounter database connection issues:

1. Verify your database connection credentials
2. Ensure the database server allows connections from Render's IP addresses
3. Check if your database provider requires SSL connections (for secure connections)

## Security Notes

- Never commit your `.env` file with real credentials
- Use strong passwords for your database
- Consider using connection pooling for production deployment 