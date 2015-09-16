# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


class RegistrationFormTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.creative-city-berlin.de/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_registration_form(self):
        driver = self.driver
        driver.get(self.base_url + "/de/register/")
        Select(driver.find_element_by_id("id_prefix")).select_by_visible_text("Herr")
        driver.find_element_by_id("id_first_name").clear()
        driver.find_element_by_id("id_first_name").send_keys("Tiago")
        driver.find_element_by_id("id_last_name").clear()
        driver.find_element_by_id("id_last_name").send_keys("Henriques")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("qwerty@studio38.org")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("qwerty")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("henhenhen")
        driver.find_element_by_id("id_password_confirm").clear()
        driver.find_element_by_id("id_password_confirm").send_keys("henhenhen")
        driver.find_element_by_id("id_CI_942").click()
        driver.find_element_by_id("id_privacy_policy").click()
        driver.find_element_by_id("id_terms_of_use").click()
        driver.find_element_by_id("id_newsletter_1").click()
        driver.find_element_by_id("id_newsletter_3").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
        self.assertEqual("Creative City Berlin - Sie haben es fast geschafft.", driver.title)
        try:
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.col3_content.clearfix > h1"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual("Sie haben es fast geschafft.",
                             driver.find_element_by_css_selector("div.col3_content.clearfix > h1").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertTrue(self.is_element_present(By.XPATH, "//div[@id='main']/div[3]/div/div/p[2]/strong"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual(u"Bitte schauen Sie auch in Ihren Spamordner nach der Bestätigungsmail.",
                             driver.find_element_by_xpath("//div[@id='main']/div[3]/div/div/p[2]/strong").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

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
