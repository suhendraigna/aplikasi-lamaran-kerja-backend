

class DomainException(Exception):
    """
    Base exception untuk seluruh error bisnis (domain).
    """
    
    def __init__(self, kode, pesan):
        self.kode = kode
        self.pesan = pesan
        super().__init__(pesan)
