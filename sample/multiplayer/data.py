class SendData:
    """Just a class to store data"""
    def __init__(self, tag : str, **kwargs) -> None:
        self.tag = tag
        self.data = dict(kwargs)