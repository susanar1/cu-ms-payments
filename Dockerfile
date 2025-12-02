# IMAGEN BASE
FROM python:3.14-alpine
 
# INSTRUCCIONES
WORKDIR /app
 
# Copiar el archivo de la aplicación
COPY app.py .
 
# Exponer el puerto 3000
EXPOSE 3000

# ENTRYPOINT
CMD ["python", "app.py"]
 