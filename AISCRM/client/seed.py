from .models import clients
from faker import Faker 

fake = Faker()


def seed_db(n):
    for i in range(0, n):
        clients.objects.create(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email = fake.email(),
            company_name = fake.company(),
            phone = fake.unique.random_number(digits=10),
            Alternate_no = fake.unique.random_number(digits=10),
            amc_client = fake.boolean(),
            GST_no = fake.unique.random_number(digits=15),
        )
