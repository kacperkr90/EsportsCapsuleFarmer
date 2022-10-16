from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from EsportsCapsuleFarmer.Container.TearDown import shutdown_gracefully


class Rewards:
    def __init__(self, log, driver, multiplier) -> None:
        self.log = log
        self.driver = driver
        self.multiplier = multiplier

    def findRewardsCheckmark(self):
        """
        Checks if the user is currently eligible to receive rewards.
        """
        wait = WebDriverWait(self.driver, 15 * self.multiplier)
        try:
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div[class=status-summary] g")))
        except TimeoutException:
            return False
        return True

    @shutdown_gracefully()
    def checkRewards(self, url, retries=5):
        splitUrl = url.rsplit('/',1)
        match = splitUrl[1] if 1 < len(splitUrl) else "Match "
        for i in range(retries):
            if self.findRewardsCheckmark():
                self.log.info(f"{match} is eligible for rewards ✓")
                break
            else:
                if i < 4:
                    self.log.warning(f"{match} is not eligible for rewards. Retrying...")
                    self.driver.get(url)
                else:
                    self.log.error(f"{match} is not eligible for rewards") 
