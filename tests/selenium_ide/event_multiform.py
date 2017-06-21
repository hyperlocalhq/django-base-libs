# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class EventMultiform(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_event_multiform(self):
        driver = self.driver
        driver.get(self.base_url + "/en/events/add/")
        driver.find_element_by_id("id_email_or_username").clear()
        driver.find_element_by_id("id_email_or_username").send_keys("olifante")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("abcdef1234")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_id("id_title_de").clear()
        driver.find_element_by_id("id_title_de").send_keys("Wie erreiche ich mein Publikum? - Dr. Helen Adkins")
        Select(driver.find_element_by_id("id_event_type")).select_by_visible_text("Seminar/Workshop/Kurs")
        Select(driver.find_element_by_id("id_event_times-0-label")).select_by_visible_text("Veranstaltung")
        Select(driver.find_element_by_id("id_event_times-0-start_dd")).select_by_visible_text("28")
        Select(driver.find_element_by_id("id_event_times-0-start_mm")).select_by_visible_text("September")
        Select(driver.find_element_by_id("id_event_times-0-start_yyyy")).select_by_visible_text("2015")
        Select(driver.find_element_by_id("id_event_times-0-start_hh")).select_by_visible_text("14")
        Select(driver.find_element_by_id("id_event_times-0-start_ii")).select_by_visible_text("30")
        driver.find_element_by_id("id_venue_text").clear()
        driver.find_element_by_id("id_venue_text").send_keys("Bildungswerk des bbk berlin")
        driver.find_element_by_id("id_phone_area").clear()
        driver.find_element_by_id("id_phone_area").send_keys("30")
        driver.find_element_by_id("id_phone_number").clear()
        driver.find_element_by_id("id_phone_number").send_keys("230 899 40")
        driver.find_element_by_id("id_organizer_ind_2").click()
        driver.find_element_by_id("id_url0_link").clear()
        driver.find_element_by_id("id_url0_link").send_keys("http://www.bbk-bildungswerk.de/con/cms/front_content.php/idcat.107")
        driver.find_element_by_xpath("//input[@value='NEXT']").click()
        driver.find_element_by_id("id_description_de").clear()
        driver.find_element_by_id("id_description_de").send_keys(u"Einladung / Presse / Karte / Katalog / Ausstellung / Event\n\nOb für Einzel- oder Gruppenausstellungen, offene Ateliers oder Events, Besucher_innen müssen eingeladen werden. Hat man die Adresse des ersehnten Gastes, ist es noch lange nicht so, dass er/sie sich auf den Weg macht.\nDie Einladung – gedruckt, digital oder beides – ist ein Basiswerkzeug, um auf sich aufmerksam zu machen. Nur zu häufig landet die Einladung unbeachtet im Papierkorb. Wie kann man das verhindern? Wie kann eine Aussendung effektiv eingesetzt werden? Wann soll sie verschickt werden? Was soll dazu gelegt werden? Welche sonstigen Ansprachen gibt es noch?\n\nDie Teilnehmer_innen werden gebeten, zwei in ihren Augen geglückte Einladungen (zu einer eigenen oder fremden Ausstellung) zum Workshop mitzubringen.\n\n\n\n\nMontag, 28.09.2015 von 14:30-18:30 Uhr              \n                                                                               \nAnmeldung unter: http://www.bbk-bildungswerk.de/con/cms/front_content.php?idart=3923&refId=415\n\nDieses Angebot des Bildungswerks wird mit Geldern des Europäischen Sozialfonds (ESF) unterstützt.")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_id("id_fees_de").clear()
        driver.find_element_by_id("id_fees_de").send_keys(u"Teilnahmegebühr: 25 €")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_css_selector("span.pic").click()
        driver.find_element_by_id("id_CI_101").click()
        driver.find_element_by_id("id_tags").clear()
        driver.find_element_by_id("id_tags").send_keys(u"Öffentlichkeitsarbeit")
        driver.find_element_by_css_selector("input.primaryAction").click()
        self.assertRegexpMatches(driver.find_element_by_xpath("//div[@id='main']/div[3]/div/div/form/h3[2]").text, r"^exact:Wie erreiche ich mein Publikum[\s\S] - Dr\. Helen Adkins$")
        self.assertEqual(u"Bildungswerk des bbk berlin\n Köthener Str. 44\n 10963 Berlin\n Germany", driver.find_element_by_css_selector("address").text)
        self.assertEqual("+ 49 -30-230 899 40", driver.find_element_by_xpath("//div[@id='main']/div[3]/div/div/form/div[3]/dl[2]/dd").text)
        self.assertEqual(u"Teilnahmegebühr: 25 €", driver.find_element_by_xpath("//div[@id='main']/div[3]/div/div/form/div[3]/dl[4]/dd").text)
        self.assertEqual("Tiago Henriques", driver.find_element_by_link_text("Tiago Henriques").text)
        self.assertEqual("Fine Art", driver.find_element_by_xpath("//div[@id='main']/div[3]/div/div/form/div[7]/dl/dd").text)
        self.assertEqual(u"Öffentlichkeitsarbeit", driver.find_element_by_xpath("//div[@id='main']/div[3]/div/div/form/div[7]/dl/dd[2]").text)
        driver.find_element_by_css_selector("input.primaryAction").click()
        self.assertRegexpMatches(driver.title, r"^exact:Kreatives Brandenburg - Wie erreiche ich mein Publikum[\s\S] - Dr\. Helen Adkins$")
        self.assertRegexpMatches(driver.title, r"^exact:Kreatives Brandenburg - Wie erreiche ich mein Publikum[\s\S] - Dr\. Helen Adkins$")
        self.assertEqual("September 28, 2015 14:30", driver.find_element_by_css_selector("abbr.dtstart").text)
        self.assertEqual("Bildungswerk des bbk berlin", driver.find_element_by_link_text("Bildungswerk des bbk berlin").text)
        self.assertEqual(u"Köthener Str. 44,", driver.find_element_by_css_selector("span.street-address").text)
        self.assertEqual("10963", driver.find_element_by_css_selector("span.postal-code").text)
        self.assertEqual("Berlin,", driver.find_element_by_css_selector("span.locality").text)
        self.assertEqual("Germany", driver.find_element_by_css_selector("span.country-name").text)
        self.assertEqual("+49-30-230 899 40", driver.find_element_by_css_selector("span.value").text)
        self.assertEqual("http://www.bbk-bildungswerk.de/con/cms/front_content.php/idcat.107", driver.find_element_by_link_text("http://www.bbk-bildungswerk.de/con/cms/front_content.php/idcat.107").text)
        for i in range(60):
            try:
                if re.search(r"^exact:Kreatives Brandenburg - Wie erreiche ich mein Publikum[\s\S] - Dr\. Helen Adkins$", driver.title): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if re.search(r"^exact:Kreatives Brandenburg - Wie erreiche ich mein Publikum[\s\S] - Dr\. Helen Adkins$", driver.title): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("Workshop", driver.find_element_by_xpath("//div[@id='dyn_identity']/div/dl[2]/dd").text)
        self.assertEqual(u"Teilnahmegebühr: 25 €", driver.find_element_by_css_selector("#dyn_fees_opening_hours > div.section-details > dl > dd").text)
        self.assertEqual("Tiago Henriques", driver.find_element_by_css_selector("#dyn_organizer > div.section-details > dl > dd > a").text)
        self.assertEqual("Fine Art", driver.find_element_by_css_selector("#dyn_categories > div.section-details > dl > dd").text)
        self.assertEqual(u"Öffentlichkeitsarbeit", driver.find_element_by_xpath("//div[@id='dyn_categories']/div/dl[2]/dd").text)
        self.assertEqual("Regional", driver.find_element_by_xpath("//div[@id='dyn_categories']/div/dl[3]/dd").text)
        driver.find_element_by_xpath("//div[@id='main']/div[2]/div/div/div/ul/li[2]/a/span").click()
    
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
