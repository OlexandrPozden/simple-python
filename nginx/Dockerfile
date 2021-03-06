FROM nginx
#configuration

RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d/
#content, comment out the ones you dont need!
#COPY ./*.html /usr/share/nginx/html/

COPY ./static/ /usr/share/nginx/html/static/
#copy ./*.png /usr/share/nginx/html/
#COPY ./static/js*.js /usr/share/nginx/html/static/

COPY ./static/favicon.ico /usr/share/nginx/html/
#COPY source dest