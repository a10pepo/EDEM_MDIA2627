FROM nginx:1.27-alpine

# nginx sustituye ${BACKEND_URL} al arrancar (plantillas en /etc/nginx/templates)
ENV BACKEND_URL=http://backend:8000

COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY index.html styles.css app.js estaciones.json /usr/share/nginx/html/

EXPOSE 80
