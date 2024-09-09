# NFL TPS Data Collection and Visualization

This Python app collects and visualizes transaction data based on NFL season phases (Pre-season, Regular Season, Playoffs, etc.). The app includes cron jobs to run two Python scripts:
- `collect_data.py`: Collects transactions per minute (TPM) and transactions per second (TPS) data every day at 09:00 AM.
- `plot_data.py`: Generates TPS charts every day at 09:30 AM.

Additionally, you can log in to the container to manually run these scripts using `bash`.

## Features

- **Configurable Database Connection**: Database connection settings (host, user, password, database name, port) can be passed as environment variables or through an `.env` file.
- **Single Container**: The app runs in a single container that schedules cron jobs and provides a bash interface for manual execution.
- **Cron Job Automation**: Automatically schedules the scripts to run at specified times:
  - `collect_data.py` runs every day at 09:00 AM.
  - `plot_data.py` runs every day at 09:30 AM.
- **Data Volume Mounting**: The `/app/data` directory in the container is mounted to a `local-data` directory on your host machine, allowing you to easily access the generated data and charts.
- **Log Management**: Cron job logs are stored in a `local-logs` directory on your host machine.

## Prerequisites

- Docker installed
- PostgreSQL database setup with access permissions for the app

## Environment Variables

You can configure environment variables for database connection either by setting them directly on your host system or by using an `.env` file.

### Option 1: Define Environment Variables on Your Host Machine

Before running `docker-compose`, set environment variables on your host machine. For example, on Linux or macOS:

```bash
export DB_HOST=your_custom_host
export DB_USER=your_custom_user
export DB_PASS=your_custom_password
export DB_NAME=your_custom_database
export DB_PORT=5432
```

On Windows (PowerShell):

```powershell
$env:DB_HOST="your_custom_host"
$env:DB_USER="your_custom_user"
$env:DB_PASS="your_custom_password"
$env:DB_NAME="your_custom_database"
$env:DB_PORT="5432"
```

### Option 2: Use an `.env` File

Create an `.env` file in the same directory as your `docker-compose.yml` file with the following content:

```bash
DB_HOST=your_custom_host
DB_USER=your_custom_user
DB_PASS=your_custom_password
DB_NAME=your_custom_database
DB_PORT=5432
```

Docker Compose will automatically load this file.

## Usage with Docker Compose

### Step 1: Clone the Repository

```bash
git clone https://github.com/trustlreis/nfl-transaction-monitor.git
cd nfl-transaction-monitor
```

### Step 2: Update the `docker-compose.yml`

If you prefer not to use the `.env` file, ensure that your `docker-compose.yml` is configured to use host environment variables:

```yaml
services:
  nfl-tps-app:
    ...
    environment:
      DB_HOST: ${DB_HOST}                # Referencing environment variables from the host
      DB_USER: ${DB_USER}
      DB_PASS: ${DB_PASS}
      DB_NAME: ${DB_NAME}
      DB_PORT: ${DB_PORT}
    ...
```

### Step 3: Build the Docker Image

Run the following command to build the Docker image:

```bash
docker-compose build
```

### Step 4: Start the Container

Run the following command to start the container in detached mode:

```bash
docker-compose up -d
```

### Step 5: Verify Cron Job Logs

To check the cron job logs, use the following command:

```bash
docker-compose exec nfl-tps-app tail -f /var/log/cron.log
```

### Step 6: Manually Run the Scripts

If you need to log into the container and manually run the scripts:

```bash
docker-compose exec nfl-tps-app bash
```

Once inside the container, you can run the Python scripts:

```bash
python collect_data.py
python plot_data.py
```

### Step 7: Stop the Container

To stop and remove the running container:

```bash
docker-compose down
```

## Folder Structure

```bash
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config
│   ├── config.yaml                # YAML file for backup config if environment variables are not used
├── collect_data.py                # Script to collect transaction data
├── plot_data.py                   # Script to generate TPS charts
├── local-data/                    # Mounted directory for storing generated data and charts
├── local-logs/                    # Mounted directory for cron job logs (updated to local-logs)
└── README.md                      # This documentation
```

## Cron Jobs

The following cron jobs are configured inside the container:

- **Collect Data**: `collect_data.py` runs every day at 09:00 AM.
- **Generate Charts**: `plot_data.py` runs every day at 09:30 AM.

Cron job logs are available in the `local-logs/` directory on your host machine.