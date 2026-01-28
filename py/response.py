class Response:
    """
    自訂的回應類別
    """

    def __init__(self, message='', data=None):
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            'message': self.message,
            'data': self.data,
        }
