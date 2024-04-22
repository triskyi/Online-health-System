#!/bin/bash

# Activate virtual environment
source /path/to/your/virtualenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if applicable)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
