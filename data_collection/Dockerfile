# Use the official Apache Airflow image as a base image
FROM apache/airflow:2.2.0

# Copy requirements and install them as root
COPY requirements.txt /tmp/requirements.txt

# Copy dependecies and install them as root
COPY install_dependencies.sh /tmp/install_dependencies.sh
RUN sh /tmp/install_dependencies.sh

# Copy the custom configuration file into the container
COPY airflow.cfg /usr/local/airflow/airflow.cfg

# Set the AIRFLOW_HOME variable
ENV AIRFLOW_HOME=/usr/local/airflow

# Change to root user to change permissions and perform operations requiring higher privileges
USER root

# Copy drivers and install them as root
COPY driver_odbc_linux.sh /tmp/driver_odbc_linux.sh
RUN sh /tmp/driver_odbc_linux.sh

# Change permissions of AIRFLOW_HOME directory
RUN mkdir -p $AIRFLOW_HOME && chown -R airflow: $AIRFLOW_HOME

# Copy the start-airflow.sh script into the image and make it executable
COPY start-airflow.sh /usr/local/bin/start-airflow.sh
RUN chmod +x /usr/local/bin/start-airflow.sh

# Switch back to airflow user for the remaining operations
USER airflow

# Copy your dags (spider) to the image
COPY --chown=airflow:airflow automatisation/dags /usr/local/airflow/dags

# Copy the Scrapy project
COPY box_office /opt/scrapy_project

# Set Airflow to use the SequentialExecutor
ENV AIRFLOW__CORE__EXECUTOR=SequentialExecutor

# Initialize the database
RUN airflow db init

# Create a user for accessing the web interface (optional)
RUN airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname Admin \
    --role Admin \
    --email admin@example.com

# Expose the web server's port
EXPOSE 8080

# Start the web server and scheduler
ENTRYPOINT ["/usr/local/bin/start-airflow.sh"]
