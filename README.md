# HM Electronic
A multipurpose website(shop & blog & customer support) for HM Electronic( sales representative )

## Features
- Implemented for performing all the tasks of a shop website.
- Implemented for performing all the tasks of a blog website.
- Implementing the Persian (Shamsi) date using both the "django-jalali" and "django-jalali-date" packages. However, personally, I prefer using the "django-jalali-date" package.
- Custome admin panel.
- Connectet to the <a href='https://next.zarinpal.com/'>Zarinpal</a> payment gateway.
- Connected to the <a href='https://kavenegar.com/'>Kavenegar</a> SMS sending portal.
- PDF & CSV output for users order.
- Cache System (using memcached) .
- Special API for Torob.com
- Using Celery and flower (flower for monitoring & Redis for Celery back) .
- Products discount Countdown .
- Send Email through admin panel.
- Implementing a admin notification system using Package <a href='https://github.com/amirhamiri/django-admin-notification'>django-admin-notification</a> for new orders.
- Comments & Reply comment
- Authentication system & forgot password
- Number of Products and Blogs visit
- Block list IPs & Block list user agents
- Custome user model
- ETC

## Usage :
```bash
git clone https://github.com/Aron-S-G-H/hmelectronic.ir.git
pip install -r requirements.txt
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py runserver # and see in 127.0.0.1:8000
# In another terminal, enter the following command to run celery
celery -A Electronic worker -l info
# Again in another terminal, enter the following command to run flower
celery -A Electronic flower # and see localhost:5555 for monitoring
# you also need Redis as broker and back
```
