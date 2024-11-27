class Bank:
    def __init__(self, api_base_url: str, bank_identification_number: str) -> None:
        self.api_base_url = api_base_url
        self.bank_identification_number = bank_identification_number
