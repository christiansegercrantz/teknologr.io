from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from registration.forms import format_programmes
import string
import random


def _gen_rnd_str(length=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choices(chars, k=length))


class RegistrationTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(RegistrationTest, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(RegistrationTest, self).tearDown()

    def test_register(self):
        self.driver.get(self.live_server_url + reverse('registration.views.home'))
        by_id = lambda form_id: self.driver.find_element_by_id(form_id)

        # Find all form inputs
        surname = by_id('id_surname')
        given_names = by_id('id_given_names')
        preferred_name = by_id('id_preferred_name')
        street_address = by_id('id_street_address')
        postal_code = by_id('id_postal_code')
        city = by_id('id_city')
        phone = by_id('id_phone')
        email = by_id('id_email')
        birth_date = by_id('id_birth_date')
        student_id = by_id('id_student_id')
        enrolment_year = by_id('id_enrolment_year')
        motivation = by_id('id_motivation')
        degree_programme = Select(self.driver.find_element_by_id('id_degree_programme_options'))

        # Fill in all form elements
        surname.send_keys(_gen_rnd_str())
        given_names.send_keys(_gen_rnd_str())
        preferred_name.send_keys(_gen_rnd_str())
        street_address.send_keys(_gen_rnd_str())
        postal_code.send_keys(_gen_rnd_str(chars=string.digits))
        city.send_keys(_gen_rnd_str())
        phone.send_keys(_gen_rnd_str(10, string.digits))
        email.send_keys('{}@email.com'.format(_gen_rnd_str()))
        birth_date.send_keys(_gen_rnd_str())
        student_id.send_keys(_gen_rnd_str())
        enrolment_year.send_keys(_gen_rnd_str(4, string.digits))
        motivation.send_keys(_gen_rnd_str())
        degree_programme.select_by_value(random.choice(format_programmes())[0])

        # Submit form
        by_id('submit_btn').click()
