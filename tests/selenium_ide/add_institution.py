# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AddInstitution(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_add_institution(self):
        driver = self.driver
        driver.get(self.base_url + "/en/institutions/add/")
        driver.find_element_by_id("id_institution_name").clear()
        driver.find_element_by_id("id_institution_name").send_keys("test institution - delete later")
        Select(driver.find_element_by_id("id_legal_form")).select_by_visible_text("AG")
        Select(driver.find_element_by_id("id_location_type")).select_by_visible_text("Hauptsitz")
        driver.find_element_by_id("id_street_address").clear()
        driver.find_element_by_id("id_street_address").send_keys(u"Rosenthaler Straße 38")
        driver.find_element_by_id("id_postal_code").clear()
        driver.find_element_by_id("id_postal_code").send_keys("10178")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("Berlin")
        Select(driver.find_element_by_id("id_country")).select_by_visible_text("Deutschland")
        driver.find_element_by_css_selector("option[value=\"DE\"]").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_id("id_OT_138").click()
        driver.find_element_by_id("id_CI_104").click()
        driver.find_element_by_id("id_BC_331").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
