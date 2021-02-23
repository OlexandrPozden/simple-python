FROM nginx:1.15.8-alpine
#configuration
COPY ./nginx.conf /etc/nginx/nginx.conf

#content, comment out the ones you dont need!
COPY ./*.html /usr/share/nginx/html/

COPY ./static/*.css /usr/share/nginx/html/static/
#copy ./*.png /usr/share/nginx/html/
COPY ./static/*.js /usr/share/nginx/html/static/