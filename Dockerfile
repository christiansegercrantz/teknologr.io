FROM python:3.5.2-alpine

# Install prereqs
RUN apk update
RUN apk add git gcc
RUN apk add openssl-dev musl-dev openldap-dev postgresql-dev

# Create directories
RUN mkdir -p /var/log/teknologr
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/teknologr

# Copy files
COPY requirements.txt start-teknologr.sh /opt/app/
RUN true
COPY .pip_cache /opt/app/pip_cache/
RUN true
COPY teknologr /opt/app/teknologr

# Set workdir
WORKDIR /opt/app

# Create systemgroup
RUN addgroup -S www-data

# Create user; no home dir, no password,
# system user, shell, and group
RUN adduser -HDS -s /bin/false -G www-data www-data

# Install pip requirements
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

# Create logfile
RUN touch /var/log/teknologr/info.log
RUN chmod -R 775 /var/log/teknologr/info.log
RUN chmod -R 775 /opt/app/start-teknologr.sh

# Chown directories
RUN chown -R www-data:www-data /opt/app
RUN chown -R www-data:www-data /var/log/teknologr

# Link teknologr log to stdout
# Commented out because of error
RUN ln -sf /dev/stdout /var/log/teknologr/info.log

# Start server
EXPOSE 8010
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-teknologr.sh"]
