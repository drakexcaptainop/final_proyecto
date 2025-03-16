PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Enable HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Secure Cookies
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',      'level': 'DEBUG',
            'propagate': True,ss': 'logging.FileHandler',
        },me': '/path/to/your/logfile.log',
    },
}
        },
    },
}
