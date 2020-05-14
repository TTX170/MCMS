#Welcome to the Meraki Configuartion Management System

This project contains my Final Year Project for De Montfort University, Usage is permited without warranty.
---
##prerequisites

1. Docker and Docker Compose
2. A Meraki Dashboard login and suitable testing network (I recomend browsing devnet.cisco.com if you don't have one)
3. An internet Connection
---
##Setup Insructions

1. Run `Docker-compose up`, wait for it to build and then ^C out of the process
2. Run `Docker-compose run web python manage.py migrate` This sets up the database
3. Run `Docker-compose run web python manage.py createsuperuser` This create you an admin user
4. Run `Docker-compose run web python manage.py generate_encryption_key` This creates an encryption key for the api key fields **If deploying to Production please use something more secure like Vault from Hashicorp**
5. Save the key you just created in envkey.env (If you don't want to use the key it generates feel free to provide your own 

---


