from selenium_driver_updater import DriverUpdater
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium import webdriver
from EsportsCapsuleFarmer.Container.SeleniumGrid import ensure_selenium_grid_readiness


class Webdriver:
    def __init__(self, log, browser, headless, remoteWdHubUrl) -> None:
        self.log = log
        self.remoteWdHubUrl = remoteWdHubUrl
        self.browser = browser
        self.headless = headless

    @ensure_selenium_grid_readiness()
    def createWebdriver(self):
        """
        Creates the web driver which is automatically controlled by the program
        """
        match self.browser:
            case "chrome":
                driverPath = DriverUpdater.install(path=".", driver_name=DriverUpdater.chromedriver, upgrade=True, check_driver_is_up_to_date=True, old_return=False)
                options = self.addWebdriverOptions(webdriver.ChromeOptions())
                service = ChromeService(driverPath)
                return webdriver.Chrome(service=service, options=options)            
            case "firefox":
                driverPath = DriverUpdater.install(path=".", driver_name=DriverUpdater.geckodriver, upgrade=True, check_driver_is_up_to_date=True, old_return=False)
                options = self.addWebdriverOptions(webdriver.FirefoxOptions())
                service = FirefoxService(driverPath)
                return webdriver.Firefox(service=service, options=options)
            case "edge":  # NO CURRENT DRIVER AVAILABLE
                driverPath = DriverUpdater.install(path=".", driver_name=DriverUpdater.edgedriver, upgrade=True, check_driver_is_up_to_date=True, old_return=False)
                options = self.addWebdriverOptions(webdriver.EdgeOptions())
                service = EdgeService(driverPath)
                return webdriver.Edge(service=service, options=options)
            case "remote":
                options = self.addWebdriverOptions(webdriver.FirefoxOptions())
                options.add_argument('--ignore-ssl-errors=yes')
                options.add_argument('--ignore-certificate-errors')
                return webdriver.Remote(command_executor=self.remoteWdHubUrl, options=options)

    def addWebdriverOptions(self, options):
        options.add_argument("log-level=3")
        if self.headless:
            options.add_argument("--headless")
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71"
            options.add_argument(f'user-agent={user_agent}')
        return options
