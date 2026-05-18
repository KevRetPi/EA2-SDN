#!/bin/bash

# 1. Generar el Dockerfile automáticamente
echo " Generando Dockerfile..."
cat <<EOF > Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EOF

# 2. Construir la imagen de Docker
echo "Construyendo la imagen Docker..."
docker build -t logistica-deportiva-app .

# 3. Detener y limpiar contenedor previo si existe (buena práctica para Jenkins)
docker stop samplerunning 2>/dev/null
docker rm samplerunning 2>/dev/null

# 4. Ejecutar el contenedor
# NOTA: Le damos el nombre 'samplerunning' porque el script de Jenkins lo buscará con ese nombre para detenerlo en su etapa 'Preparation'
echo "Ejecutando el contenedor..."
docker run --name samplerunning --env-file .env logistica-deportiva-app

# 5. Generar archivo de evidencias output.txt
echo "Generando output.txt con evidencias..."
echo "=== SALIDA DE DOCKER PS -A ===" > output.txt
docker ps -a --filter "name=samplerunning" >> output.txt
echo -e "\n=== LOGS DEL CONTENEDOR ===" >> output.txt
docker logs samplerunning >> output.txt

echo "Proceso finalizado con éxito."