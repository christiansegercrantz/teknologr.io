FROM python:3.7-buster

# Install prereqs
RUN apt-get update && apt-get install -y libsasl2-dev libldap2-dev libssl-dev libpq-dev

# Create folders
RUN mkdir -p /var/log/teknologr
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/teknologr

# Copy files to workdir
COPY requirements.txt start-teknologr.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY teknologr /opt/app/teknologr
RUN touch /var/log/teknologr/info.log

# Set workdir
WORKDIR /opt/app

# Install pip requirements
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

# Chown folders
RUN chown -R www-data:www-data /opt/app
RUN chown -R www-data:www-data /var/log/teknologr
RUN chmod -R 755 /var/log/teknologr/info.log

#Start server
EXPOSE 8010
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-teknologr.sh"]
