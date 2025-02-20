FROM python:3.10

RUN apt-get update && \
  apt-get install -y libgl1-mesa-glx && \
  rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# set env variables
ENV FLASK_ENV=development
ENV TF_FORCE_GPU_ALLOW_GROWTH=true

# declare volumes
VOLUME ["/app/processed_images", "/app/data"]

# Run app.py when the container launches
CMD ["python", "app.py"]