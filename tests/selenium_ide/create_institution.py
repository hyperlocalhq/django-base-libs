# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


class CreateInstitution(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_create_institution(self):
        driver = self.driver
        driver.get(self.base_url + "/en/institutions/add/")
        driver.find_element_by_id("id_institution_name").clear()
        driver.find_element_by_id("id_institution_name").send_keys("Selenium")
        driver.find_element_by_id("id_institution_name2").clear()
        driver.find_element_by_id("id_institution_name2").send_keys("Test")
        Select(driver.find_element_by_id("id_legal_form")).select_by_visible_text("AG")
        Select(driver.find_element_by_id("id_location_type")).select_by_visible_text("Hauptsitz")
        driver.find_element_by_id("id_location_title").clear()
        driver.find_element_by_id("id_location_title").send_keys("selenium test")
        driver.find_element_by_id("id_street_address").clear()
        driver.find_element_by_id("id_street_address").send_keys("selenium test")
        driver.find_element_by_id("id_street_address2").clear()
        driver.find_element_by_id("id_street_address2").send_keys("selenium test")
        driver.find_element_by_id("id_postal_code").clear()
        driver.find_element_by_id("id_postal_code").send_keys("selenium test")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("selenium test")
        Select(driver.find_element_by_id("id_country")).select_by_visible_text("Deutschland")
        driver.find_element_by_id("id_phone_area").clear()
        driver.find_element_by_id("id_phone_area").send_keys("12345")
        driver.find_element_by_id("id_phone_number").clear()
        driver.find_element_by_id("id_phone_number").send_keys("6789")
        driver.find_element_by_id("id_fax_area").clear()
        driver.find_element_by_id("id_fax_area").send_keys("12345")
        driver.find_element_by_id("id_fax_number").clear()
        driver.find_element_by_id("id_fax_number").send_keys("6789")
        driver.find_element_by_id("id_mobile_area").clear()
        driver.find_element_by_id("id_mobile_area").send_keys("12345")
        driver.find_element_by_id("id_mobile_number").clear()
        driver.find_element_by_id("id_mobile_number").send_keys("6789")
        driver.find_element_by_id("id_email0").clear()
        driver.find_element_by_id("id_email0").send_keys("selenium@test.com")
        Select(driver.find_element_by_id("id_url0_type")).select_by_visible_text("Web")
        driver.find_element_by_id("id_url0_link").clear()
        driver.find_element_by_id("id_url0_link").send_keys("http://selenium.tests.com")
        Select(driver.find_element_by_id("id_im0_type")).select_by_visible_text("Skype")
        driver.find_element_by_id("id_im0_address").clear()
        driver.find_element_by_id("id_im0_address").send_keys("seleniumtest")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_id("id_description_de").clear()
        driver.find_element_by_id("id_description_de").send_keys(
            "selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test.")
        driver.find_element_by_id("id_description_en").clear()
        driver.find_element_by_id("id_description_en").send_keys(
            "selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test. selenium test.")
        driver.find_element_by_id("id_avatar").clear()
        driver.find_element_by_id("id_avatar").send_keys("/Users/tiago/Desktop/runners.jpg")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_id("id_is_invoice_ok").click()
        driver.find_element_by_id("id_is_cash_ok").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_css_selector("a.open_but > b").click()
        driver.find_element_by_id("id_OT_345").click()
        driver.find_element_by_id("id_OT_307").click()
        driver.find_element_by_css_selector("#BC_en_search > h3 > a.open_but > b").click()
        driver.find_element_by_id("id_BC_82").click()
        driver.find_element_by_id("id_BC_12").click()
        driver.find_element_by_id("id_BC_5").click()
        driver.find_element_by_css_selector("#CI_en_search > h3 > a.open_but > b").click()
        driver.find_element_by_id("id_CI_102").click()
        driver.find_element_by_id("id_CI_105").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
        self.assertEqual("Kreatives Brandenburg - Registration - Institution", driver.title)
        self.assertEqual("Confirm Entered Data", driver.find_element_by_css_selector("fieldset.inlineLabels > h5").text)
        driver.find_element_by_css_selector("input.primaryAction").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
