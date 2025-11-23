# 1. Start with a lightweight Python version
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your code into the container
COPY . .

# 5. This command will be overridden by docker-compose, 
# but it's a good default.
CMD ["python", "main.py"]