from .models import clients
from faker import Faker 
from datetime import datetime, timedelta

fake = Faker()


def seed_db(n):
    for i in range(0, n):
        amc_client = fake.boolean()
        if amc_client:
            amc_start_date = fake.date_between_dates(date_start=datetime(2023, 1, 1), date_end=datetime(2023, 2, 15))
            amc_end_date = fake.date_between_dates(date_start=datetime(2023, 11, 25), date_end=datetime(2023, 12, 10))
        else:
            amc_start_date = None
            amc_end_date = None

        clients.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            company_name=fake.company(),
            phone=fake.phone_number(),
            Alternate_no=fake.unique.phone_number(),
            amc_client=amc_client,
            GST_no=fake.unique.random_number(digits=15),
            amc_start_date=amc_start_date,
            amc_end_date=amc_end_date,
        )