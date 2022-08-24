class McmcException(Exception):
    def __init__(self, message):
        super().__init__(message)

class SamplingException(Exception):
    def __init__(self, message):
        super().__init__(message)


class DecryptionException(Exception):
    def __init__(self, message):
        super().__init__(message)

class McmcFileException(Exception):
    def __init__(self, message):
        super().__init__(message)

