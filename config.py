import os
class Config():
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class Testing(Config):
    DEBUG = True
    TESTING = True

class DefaultConfig(Config):
    TESTING = False
    DEBUG = False


config_setings = {
"development": DevelopmentConfig,
"testing": Testing,
"default" : DefaultConfig
}