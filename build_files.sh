import os

def build(request):
    # Activate virtual environment
    os.system("source /vercel/path0/venv/bin/activate")
    # Install dependencies
    os.system("pip install -r /vercel/path0/requirements.txt")
    # Run migrations (if applicable)
    os.system("python /vercel/path0/manage.py migrate")
    # Collect static files
    os.system("python /vercel/path0/manage.py collectstatic --noinput")
