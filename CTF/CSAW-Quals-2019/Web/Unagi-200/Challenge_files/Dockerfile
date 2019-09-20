FROM php:7.3.5-fpm-alpine

# PHP-FPM production settings
RUN mv $PHP_INI_DIR/php.ini-production $PHP_INI_DIR/php.ini

# Software updates & installation
RUN apk update && \
    apk upgrade && \
    apk add fcgi && \
    rm -f /var/cache/apk/*

# Copy /var/www/html/
COPY ./public_html /var/www/html

# Copy flag.txt
COPY ./flag.txt /

# PHP-FPM Healthcheck
COPY ./php-fpm-healthcheck /usr/local/bin/

# Make /var/www/html/ read-only, enable PHP-FPM status page, disable PHP-FPM access.log, set PHP-FPM ondemand, and make PHP-FPM Healtcheck runnable
RUN chmod -R 555 /var/www && \
    set -xe && \
    echo "pm.status_path = /status" >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
    echo "access.log = /dev/null" >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
    echo "pm = ondemand" >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
    echo "pm.max_children = 3" >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
    echo "pm.process_idle_timeout = 10s" >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
    echo "pm.max_requests = 200" >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
    chmod 755 /usr/local/bin/php-fpm-healthcheck
