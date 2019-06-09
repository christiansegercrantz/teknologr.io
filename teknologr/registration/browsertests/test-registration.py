from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from registration.forms import format_programmes
import string
import random


class RegistrationTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(RegistrationTest, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(RegistrationTest, self).tearDown()

    def test_register(self):
        self.driver.get(self.live_server_url + reverse('registration.views.home'))

        def by_id(form_id):
            return self.driver.find_element_by_id(form_id)

        # Find all form inputs
        surname = by_id('id_surname')
        given_names = by_id('id_given_names')
        preferred_name = by_id('id_preferred_name')
        street_address = by_id('id_street_address')
        postal_code = by_id('id_postal_code')
        city = by_id('id_city')
        phone = by_id('id_phone')
        email = by_id('id_email')
        student_id = by_id('id_student_id')
        enrolment_year = by_id('id_enrolment_year')
        motivation = by_id('id_motivation')
        degree_programme = Select(self.driver.find_element_by_id('id_degree_programme_options'))
        mother_tongue = self.driver.find_element_by_css_selector('label.radio-inline:nth-child(2)')
        birth_date = by_id('id_birth_date')

        # Fill in all form elements
        surname.send_keys('Teknolog')
        given_names.send_keys('Svatta Flicka')
        preferred_name.send_keys('Svattarina')
        street_address.send_keys('Urdsgjallar 1')
        postal_code.send_keys('02150')
        city.send_keys('Esbo')
        phone.send_keys('040346863762')
        email.send_keys('svatta.teknolog@tf.fi')
        student_id.send_keys('111111')
        enrolment_year.send_keys('2019')
        motivation.send_keys('TF is bäst!')

        chosen_programme = random.choice(format_programmes())[0]
        degree_programme.select_by_value(chosen_programme)
        # We have to set the hidden input field manually as Django won't serve staticfiles in development
        self.driver.execute_script(
                'document.getElementById("id_degree_programme").value = "{}"'.format(chosen_programme))

        # Simlarly to above, we have to set the value of the required field
        mother_tongue.click()
        self.driver.execute_script('document.getElementById("id_mother_tongue").value = "Svenska"')

        # Filling in the birth date is a bit trickier due to the calendar widget
        clicked_bd = ActionChains(self.driver).move_to_element(birth_date).click()
        # As clicking the birth date component results in the middle part getting selected
        # we have to simulate a "back-tab"
        shifted_bd = clicked_bd.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        shifted_bd.send_keys('01011999').perform()

        # Submit form
        by_id('submit-btn').click()
