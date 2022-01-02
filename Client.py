


class Client:

  def __init__(self):
    self._private_key = RSA.generate(1024, random)