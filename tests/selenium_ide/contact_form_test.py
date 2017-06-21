# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


class ContactFormTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_contact_form(self):
        driver = self.driver
        driver.get(self.base_url + "/en/contact/")
        self.assertEqual("Kreatives Brandenburg - Contact us", driver.title)
        try:
            self.assertTrue(self.is_element_present(By.ID, "id_sender_name"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_sender_name").clear()
        driver.find_element_by_id("id_sender_name").send_keys("Tiago Henriques")
        try:
            self.assertTrue(self.is_element_present(By.ID, "id_sender_email"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_sender_email").clear()
        driver.find_element_by_id("id_sender_email").send_keys("henriques@studio38.com")
        try:
            self.assertTrue(self.is_element_present(By.ID, "id_contact_form_category"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        Select(driver.find_element_by_id("id_contact_form_category")).select_by_visible_text(
            "Kreatives Brandenburg (General)")
        try:
            self.assertTrue(self.is_element_present(By.ID, "id_subject"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_subject").clear()
        driver.find_element_by_id("id_subject").send_keys("Testing...")
        try:
            self.assertTrue(self.is_element_present(By.ID, "id_body"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_body").clear()
        driver.find_element_by_id("id_body").send_keys(
            "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.")
        try:
            self.assertTrue(self.is_element_present(By.ID, "id_submit"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        driver.find_element_by_id("id_submit").click()
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "h2.sub"))
        try:
            self.assertEqual("Thank you for your message", driver.find_element_by_css_selector("h2.sub").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "p.suggest"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual("Thank you for your message - we will contact you soon!",
                             driver.find_element_by_css_selector("p.suggest").text)
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
