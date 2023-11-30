import simplejson as json
import concurrent.futures as cf
import os
import logging
from datetime import datetime as dt

import requests
from pytest import fixture
from faker import Faker

from utils.testUtils import AddressParser

fakerGen = Faker(locale="en_US")
addressParser = AddressParser()

logging.basicConfig(filename="src/tests/logs/results.log", level=logging.INFO)

def apiBlaster(ip_addr:str, id:int):
    test_session = requests.Session()
    test_session.auth = ("admin", "admin")

    while True:
        print("iter", id)
        fuzz_addresses_us = list(map(lambda address: addressParser.execute(address=address), [str(fakerGen.address()).replace("\n", ", ") + ", " + fakerGen.current_country_code() for i in range(1000)]))

        for address in fuzz_addresses_us:
            req = test_session.post(f"http://{ip_addr}/api/address/modify/add", json=json.dumps(address))

            try:
                key = test_session.get(f"http://{ip_addr}/api/address/search", json=json.dumps(address)).json()["responseData"]["recommendedAddresses"][0]["key"]
                test_session.post(f"http://{ip_addr}/api/address/modify/delete", json = json.dumps({"key": key}))
            except Exception:
                pass
            
            try:
                if req.status_code in [400, 500] and address["address"]["stateProv"] not in ["", "AE", "AP", "AA"]:
                    logging.info(f"{req.status_code} -- {dt.now()} -- {address} -- {req.json()['responseStatusMsg']}")
                else: 
                    pass
            except Exception as e:
                print(e)

def runApiBlast(num_workers:int):
    with cf.ThreadPoolExecutor() as executor:
        for worker in range(num_workers):
            future = executor.submit(apiBlaster, ip_addr="0.0.0.0:8000", id=worker)

if __name__ == "__main__":
    runApiBlast(num_workers=round(os.cpu_count()/2))

