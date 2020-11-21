FROM python:3.7-alpine

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
COPY .pip_cache /opt/app/pip_cache/
COPY teknologr /opt/app/teknologr

# Set workdir
WORKDIR /opt/app

# Create user
RUN addgroup --system www-data
RUN adduser --no-create-home --disabled-password --system --shell /bin/false --ingroup www-data www-data

# Install pip requirements
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

# Chown directories
RUN chown -R www-data:www-data /opt/app
RUN chown -R www-data:www-data /var/log/teknologr

# Create logfile
RUN touch /var/log/teknologr/info.log
RUN chmod -R 775 /var/log/teknologr/info.log
RUN chmod -R 775 /opt/app/start-teknologr.sh

# Link teknologr log to stdout
RUN ln -sf /dev/stdout /var/log/teknologr/info.log

# Start server
EXPOSE 8010
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-teknologr.sh"]
