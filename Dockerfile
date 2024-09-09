# Use the official Python image
FROM python:3.9-slim

# Install required packages: cron, bash, and necessary dependencies
RUN apt-get update && \
    apt-get install -y cron bash && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set environment variables (replace these with your values)
ENV DB_HOST=your_custom_host
ENV DB_USER=your_custom_user
ENV DB_PASS=your_custom_password
ENV DB_NAME=your_custom_database
ENV DB_PORT=5432

# Copy Python requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Set up crontab
RUN echo "0 9 * * * /usr/local/bin/python /app/collect_data.py >> /var/log/cron.log 2>&1" > /etc/cron.d/data-collection-cron \
    && echo "30 9 * * * /usr/local/bin/python /app/plot_data.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/data-collection-cron \
    && chmod 0644 /etc/cron.d/data-collection-cron \
    && crontab /etc/cron.d/data-collection-cron

# Ensure cron.log is created and accessible
RUN touch /var/log/cron.log

# Make the data directory accessible to mount as a volume
VOLUME /app/data

# Set bash as the default command (allows manual login)
CMD ["bash"]
