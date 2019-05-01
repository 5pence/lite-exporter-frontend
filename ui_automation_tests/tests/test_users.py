from selenium import webdriver
import unittest
import datetime
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.exporter_hub_page import ExporterHubPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.applications_page import ApplicationsPage
import helpers.helpers as utils
import pytest
import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@pytest.mark.parametrize("user_id","")

@pytest.fixture(scope="function")
def open_exporter_hub(driver, url):
    # navigate to the application home page
    driver.get(url)
    # driver.maximize_window()
    # assert driver.title == "Exporter Hub - LITE"
    log.info(driver.current_url)


def test_add_users(driver, open_exporter_hub, url):
    user_id = datetime.datetime.now().strftime("%m%d%H%M")
    first_name = "Test"
    last_name = "User" + user_id
    full_name = first_name + last_name
    email = full_name.lower() + "@mail.com"

    # logged in exporter hub as exporter
    # Given I am a logged-in exporter on the exporter dashboard
    exporter_hub = ExporterHubPage(driver)
    log.info("logging in as test@mail.com")
    exporter_hub.login("test@mail.com", "password")

    # I want to add a user # Then I should have an option to manage users
    exporter_hub.click_users()

    # When I choose the option to manage users # Then I should see the current user for my company
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='test@mail.com']/following-sibling::td[text()='active']")

    # And I should have the ability to add a new user # And I can insert an name, last name email and password for user
    exporter_hub.click_add_a_user_btn()
    exporter_hub.enter_first_name(first_name)
    exporter_hub.enter_last_name(last_name)
    exporter_hub.enter_email(email)
    exporter_hub.enter_password("password")

    # When I Save
    exporter_hub.click_save_and_continue()

    # Then I return to "Manage users"
    # And I can see the original list of users
    assert driver.find_element_by_tag_name("h1").text == "Users", \
        "Failed to return to Users list page after Adding user"

    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + email + "']/following-sibling::td[text()='active']")


def test_deactivate_users(driver, url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(url)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")
    else:
        exporter_hub.go_to(url)

    full_name = "Test user_1"
    email = "testuser_1@mail.com"
    password = "1234"

    # Given I am a logged-in user
    # *I want to* deactivate users
    # When I choose the option to manage users
    exporter_hub.click_users()

    # I should have the option to deactivate an active user # edit link, and link from user name
    exporter_hub.click_edit_for_user(email)
    # exporter_hub.click_user_name_link("Test User")

    # When I choose to deactivate an active user # Then I return to "Manage users"
    exporter_hub.click_deactivate_btn()

    # And I can see that the user is now deactivated
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + email + "']/following-sibling::td[text()='deactivated']")
    # Given I am a deactivated user # When I attempt to log in # And I cannot log in
    exporter_hub.logout()
    exporter_hub.login(email, password)
    assert "Enter a valid email/password" in driver.find_element_by_css_selector(".govuk-error-message").text


def test_reactivate_users(driver, open_exporter_hub, url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(url)
    log.info("logging in as test@mail.com")
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")
    else:
        exporter_hub.go_to(url)

    full_name = "Test user_1"
    email = "testuser_1@mail.com"
    password = "1234"

    # As a logged in user
    # I want to reactivate users who have previously been deactivated
    # So that returned users can perform actions in the system
    # Then I should see the current active and deactivated users
    # And I should have the option to activate a deactivated user
    exporter_hub.click_users()
    exporter_hub.click_user_name_link(full_name)

    # When I choose to activate a deactivated user
    # Then I am asked "Are you sure you want to re-activate user <insert name>?"
    exporter_hub.click_reactivate_btn()

    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + email + "']/following-sibling::td[text()='active']"),\
        "user should status was expected to be active"

    exporter_hub.logout()
    exporter_hub.login(email, password)

    # Given I am a reactivated I can log in
    assert driver.title == "Exporter Hub - LITE"


def test_teardown(driver):
    driver.quit()