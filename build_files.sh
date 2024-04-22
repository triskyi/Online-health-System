#!/bin/bash

# Activate virtual environment
source C:/Users/User/Envs/votenv/Scripts/activate

# Set up environment variables
export PATH="$VIRTUAL_ENV/Scripts:$PATH"

# Install dependencies
pip install -r requirements.txt

# Run migrations (if applicable)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
