# Step 1: Use an official, lightweight Python image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy only the dependencies file first for caching
COPY requirements.txt .

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code
COPY . .

# Step 6: Expose the port the app will run on
EXPOSE 5000

# Step 7: The command to run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]