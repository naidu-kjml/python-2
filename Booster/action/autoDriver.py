# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.select import Select


class AutomateDriver(object):
    """
    a simple demo of selenium framework tool
    """

    def __init__(self,driver):

        self.driver = driver


    def clearCookies(self):
        """
        clear all cookies after driver init
        """
        self.driver.delete_all_cookies()

    def refreshBrowser(self):
        self.driver.refresh()

    def maximizeWindow(self):
        self.driver.maximize_window()

    def navigate(self, url):
        self.driver.get(url)

    def quitBrowser(self):
        self.driver.quit()

    def closeBrowser(self):
        self.driver.close()

    def getElement(self, selector):
        """
        to locate element by selector
        :arg
        selector should be passed by an example with "i,xxx"
        "x,//*[@id='langs']/button"
        :returns
        DOM element
        """
        if ',' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split(',')[0]
        selector_value = selector.split(',')[1]

        if selector_by == "i" or selector_by == 'id':
            element = self.driver.find_element_by_id(selector_value)
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            element = self.driver.find_element_by_xpath(selector_value)
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        elif selector_by == "a" or selector_by == 'alert':
            element = self.driver.find_element_by_xpath(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    def type(self, selector, text):
        """
        Operation input box.

        Usage:
        driver.type("i,el","selenium")
        """
        el = self.getElement(selector)
        el.clear()
        el.send_keys(text)

    def click(self, selector):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("i,el")
        """
        el = self.getElement(selector)
        el.click()

    def selectByIndex(self, selector, index):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.select_by_index("i,el")
        """
        el = self.getElement(selector)
        Select(el).select_by_index(index)

    def clickByText(self, text):
        """
        Click the element by the link text

        Usage:
        driver.click_text("新闻")
        """
        self.getElement('p,' + text).click()

    def submit(self, selector):
        """
        Submit the specified form.

        Usage:
        driver.submit("i,el")
        """
        el = self.getElement(selector)
        el.submit()

    def executeJs(self, script):
        """
        Execute JavaScript scripts.

        Usage:
        driver.js("window.scrollTo(200,1000);")
        """
        self.driver.execute_script(script)

    def getAttribute(self, selector, attribute):
        """
        Gets the value of an element attribute.

        Usage:
        driver.get_attribute("i,el","type")
        """
        el = self.getElement(selector)
        return el.getAttribute(attribute)

    def getText(self, selector):
        """
        Get element text information.

        Usage:
        driver.get_text("i,el")
        """
        el = self.getElement(selector)
        return el.text

    def getDisplay(self, selector):
        """
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("i,el")
        """
        el = self.getElement(selector)
        return el.is_displayed()

    def getTitle(self):
        '''
        Get window title.

        Usage:
        driver.get_title()
        '''
        return self.driver.title

    def getUrl(self):
        """
        Get the URL address of the current page.

        Usage:
        driver.get_url()
        """
        return self.driver.current_url

    def acceptAlert(self):
        '''
            Accept warning box.

            Usage:
            driver.accept_alert()
            '''
        self.driver.switch_to.alert.accept()
    
    def getAlertText(self):
        return self.driver.switch_to.alert.text

    def dismissAlert(self):
        '''
        Dismisses the alert available.

        Usage:
        driver.dismissAlert()
        '''
        self.driver.switch_to.alert.dismiss()

    def implicitlyWait(self, secs):
        """
        Implicitly wait. All elements on the page.

        Usage:
        driver.implicitly_wait(10)
        """
        self.driver.implicitly_wait(secs)

    def switchFrame(self, selector):
        """
        Switch to the specified frame.

        Usage:
        driver.switch_to_frame("i,el")
        """
        el = self.getElement(selector)
        self.driver.switch_to.frame(el)

    def switchDefaultFrame(self):
        """
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        driver.switch_to_frame_out()
        """
        self.driver.switch_to.default_content()

    def openNewWindow(self, selector):
        '''
        Open the new window and switch the handle to the newly opened window.

        Usage:
        driver.open_new_window()
        '''
        original_windows = self.driver.current_window_handle
        el = self.getElement(selector)
        el.click()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_windows:
                self.driver._switch_to.window(handle)
                
    def get_screenshot(self,file_name):
        self.driver.get_screenshot_as_file(file_name)