import os

def build(request):
    # Install dependencies
    os.system("python -m pip install -r requirements.txt")
    # Run migrations (if applicable)
    os.system("python /vercel/path0/manage.py migrate")
    # Collect static files
    os.system("python /vercel/path0/manage.py collectstatic --noinput")
