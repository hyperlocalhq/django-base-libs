# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class EventMultiform2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_event_multiform2(self):
        driver = self.driver
        driver.find_element_by_id("id_email_or_username").clear()
        driver.find_element_by_id("id_email_or_username").send_keys("olifante")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("abcdef1234")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.get(self.base_url + "/en/events/add/")
        driver.find_element_by_id("id_title_de").clear()
        driver.find_element_by_id("id_title_de").send_keys("Auflagen,Editionen, Multiples")
        Select(driver.find_element_by_id("id_event_type")).select_by_visible_text("Seminar/Workshop/Kurs")
        Select(driver.find_element_by_id("id_event_times-0-start_dd")).select_by_visible_text("10")
        Select(driver.find_element_by_id("id_event_times-0-start_mm")).select_by_visible_text("September")
        Select(driver.find_element_by_id("id_event_times-0-start_yyyy")).select_by_visible_text("2015")
        Select(driver.find_element_by_id("id_event_times-0-start_hh")).select_by_visible_text("15")
        Select(driver.find_element_by_id("id_event_times-0-start_ii")).select_by_visible_text("00")
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
        driver.find_element_by_id("id_description_de").send_keys(u"Jede/r Künstler/in wird im Laufe seiner Karriere damit konfrontiert: Auflagen, Editionen und Multiples sind ein Weg, den kommerziellen Markt zu infiltrieren. Doch wie? Im Prinzip bietet die Möglichkeit der Reproduktion die Chance, Kunst für geringeres Geld anzubieten, ohne das eigene künstlerische Konzept zu verbiegen.  Drucke sind von Natur aus für Auflagen geeignet, Fotos meistens auch. Doch welches Motiv, wie groß, wie viele Exemplare? Wer Einzelblätter nicht mag, entscheidet sich für eine Edition: auch hier stehen die gleichen Grundsatzfragen an. Das Multiple wiederum, die dreidimensionale Lösung einer Auflage, stellt weitere spezifische Anforderungen, u. a. die Frage der Präsentation.  Sich aus Existenzsicherungsgründen einem zugänglicheren Marktsegment öffnen zu wollen bedeutet auch, sich mit kommerziellen Strategien auseinanderzusetzen. Selbst \\u201eklein und günstig\\u201c verkauft sich nicht automatisch. Bei allen Auflagenobjekten stehen die sinnfälligen Fragen an: Wo produziere ich? Wie viel kostet das? Wer zahlt dafür? Wie viel Geld kann im Verkauf verlangt werden?  Nach einer allgemeinen Einführung werden konkrete Fragen der Teilnehmer besprochen.    Montag, Donnerstag, 10.09.2015 von 15-19 Uhr  Anmeldung unter: http://www.bbk-bildungswerk.de/con/cms/front_content.php?idart=3921&refId=415  Dieses Angebot des Bildungswerks wird mit Geldern des Europäischen Sozialfonds (ESF) unterstützt.")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_id("id_fees_de").clear()
        driver.find_element_by_id("id_fees_de").send_keys(u"Teilnahmegebühr: 25 €")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_css_selector("span.pic").click()
        driver.find_element_by_id("id_CI_101").click()
        driver.find_element_by_id("id_tags").clear()
        driver.find_element_by_id("id_tags").send_keys("Auflagen, Editionen")
        driver.find_element_by_css_selector("input.primaryAction").click()
        driver.find_element_by_css_selector("input.primaryAction").click()
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
