import yaml
from EsportsCapsuleFarmer.Container.EnvUtils import read_boolean, read_string, read_int, is_containerized

class Config():
    def __init__(self, log, args) -> None:
        self.log = log
        self.args = args
        self.hasAutoLogin = False
        self.isHeadless = False
        self.username = "NoUsernameInConfig" # None
        self.password = "NoPasswordInConfig" # None
        self.browser = args.browser
        self.delay = args.delay
        self.multiplier = 1
        self.remoteWdHubUrl = ""

    def getArgs(self):
        return self.hasAutoLogin, self.isHeadless, self.username, self.password, self.browser, self.delay,\
               self.multiplier, self.remoteWdHubUrl

    def getAutoLogin(self):
        return self.hasAutoLogin

    def getIsHeadless(self):
        return self.isHeadless

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getBrowser(self):
        return self.browser

    def getDelay(self):
        return self.delay

    def getMultiplier(self):
        return self.multiplier

    def getRemoteWdHubUrl(self):
        return self.remoteWdHubUrl

    def openConfigFile(self, filepath):
        with open(filepath, "r",  encoding='utf-8') as f:
            return yaml.safe_load(f)

    def readConfig(self):
        if is_containerized():
            return self.readConfigFromEnv()
        return self.readConfigFromFile()

    def readConfigFromFile(self):
        try:
            config = self.openConfigFile(self.args.configPath)
            self.log.info(f"Using configuration from: {self.args.configPath}")
            if "autologin" in config and config["autologin"]["enable"]:
                self.username = config["autologin"]["username"]
                self.password = config["autologin"]["password"]
                self.hasAutoLogin = True
            if "headless" in config:
                self.isHeadless = config["headless"]
            if "browser" in config and config["browser"] in ['chrome', 'firefox', 'edge']:
                self.browser = config["browser"]
            if "delay" in config:
                self.delay = int(config["delay"])
        except FileNotFoundError:
            self.log.warning("Configuration file not found. IGNORING...")
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
            self.log.warning("Invalid configuration file. IGNORING...")
        except KeyError:
            self.log.warning("Configuration file is missing mandatory entries. Using default values instead...")

        if not (self.isHeadless and self.hasAutoLogin):
            self.log.info("Consider using the headless mode for improved performance and stability.")

        return self

    def readConfigFromEnv(self):
        self.log.info('Capsule Farmer is running in container, will read settings from environment variables...')
        self.isHeadless = read_boolean('HEADLESS', True)
        self.hasAutoLogin = read_boolean('AUTOLOGIN_ENABLED', True)
        self.browser = read_string('BROWSER', 'remote')
        self.username = read_string('USERNAME')
        self.password = read_string('PASSWORD')
        self.delay = read_int('DELAY_IN_SECONDS', self.delay)
        self.multiplier = read_int('WAIT_VALUES_MULTIPLIER', self.multiplier)
        self.remoteWdHubUrl = read_string('REMOTE_WD_HUB_URL')
        self.log.info('Config values: [ headless=%s, autologin=%s, browser=%s, '
                      'username=*********, password=*********, '
                      'wait_values_multiplier=%s, remoteWdHubUrl=%s, delay=%s]',
                      self.isHeadless, self.hasAutoLogin, self.browser, self.multiplier, self.remoteWdHubUrl,
                      self.delay)

        return self
