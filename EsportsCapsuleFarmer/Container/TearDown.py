def shutdown_gracefully():
    def function(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as err:
                self.log.error(err)
                self.log.error("Shutting down the program gracefully.")
                self.driver.quit()
        return wrapper
    return function
