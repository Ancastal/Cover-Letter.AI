FROM python:3.7.8-slim

# Remember to expose the port your app will be listening on.
EXPOSE 8080

RUN pip install -U pip

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copy the source code
COPY . /app

# Set the working directory
WORKDIR /app

# Run the application using streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
