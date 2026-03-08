class Cliente:
  def __init__(self, nome, email):
    self.nome = nome
    self.email = email

class Conta:
  def __init__(self, numero, cliente:Cliente):
    self.numero = numero
    self.cliente = cliente
    self.__saldo = 0
    self.extrato = []

  @property
  def saldo(self):
    return self.__saldo
  
  @saldo.setter
  def saldo(self, valor):
    if valor < 0:
      raise ValueError("Valor inválido: deve ser maior que zero!")
    
    self.__saldo = valor
  
  def depositar(self, valor):
    try:
      self.saldo += valor
      self.extrato.append(f"Depósito - R${valor:.2f}")
      print(f"R${valor:.2f} Depositado com sucesso!")
    except ValueError as e:
      print(f"Erro: {e}")

  def sacar(self, valor):
    try:
      if valor <= 0:
        raise ValueError("Valor inválido: deve ser maior que zero!") 
      if self.__saldo < valor:
        raise ValueError("Saldo insuficiente!")
    
      self.saldo -= valor
      self.extrato.append(f"Saque - R${valor:.2f}")
      print(f"R${valor:.2f} sacado com sucesso!")
    except ValueError as e:
      print(f"Error: {e}")

  def obter_extrato(self):
    print("Extrato da conta")
    for i in self.extrato:
      print(i)
    print(f"Saldo atual: R${self.saldo:.2f}")

# ====================================CONTA CORRENTE=================================
class ContaCorrente(Conta):
  def __init__(self, numero, cliente:Cliente):
    super().__init__(numero, cliente)
    self.limite_especial = 500

  def sacar(self, valor):
    try:
      if valor <= 0:
        raise ValueError("Valor inválido: deve ser maior que zero!") 
      
      if self.saldo < valor:
        novo_valor = valor - self.saldo

      if novo_valor <= 500:
          self.limite_especial -= novo_valor
      else:
        raise ValueError("Saldo ou Limite Especial insuficiente!")

      if self.limite_especial >= 0:
        self.saldo += novo_valor
      else:
        raise ValueError("Limite Especial insuficiente!")
      if valor <= self.saldo:
        self.saldo -= valor
        print(f"Saque de R${valor:.2f} efetuado!")
        self.extrato.append(f"Saque - R${valor:.2f}")
      else:
        raise ValueError("Saldo insuficiente!")
      
    except ValueError as e:
      print(f"Erro: {e}")

  def obter_extrato(self):
    print("Extrato da conta")
    if self.limite_especial > 0:
      print(f"Limite Especial: R${self.limite_especial:.2f}")
    else:
      print(f"Limite Especial 100% usado!")
    for i in self.extrato:
      print(i)
    print(f"Saldo atual: R${self.saldo:.2f}")

# ====================================CONTA POUPANÇA=================================
class ContaPoupanca(Conta):
  def __init__(self, numero, cliente:Cliente):
    super().__init__(numero, cliente)
    self.taxa_saque = 2

  def sacar(self, valor):
    try:
      if valor <= 0:
        raise ValueError("Valor inválido: deve ser maior que zero!") 
      if self.saldo < valor + self.taxa_saque:
        raise ValueError("Saldo para saque insuficiente!")
    
      self.saldo -= valor
      self.saldo -= self.taxa_saque
      self.extrato.append(f"Saque - R${valor:.2f} | Taxa de Saque: R${self.taxa_saque:.2f}")
      print(f"R${valor:.2f} sacado com sucesso!")
    except ValueError as e:
      print(f"Error: {e}")
   


cliente1 = Cliente("Weslley", "weslley@gmail.com")

conta1 = Conta("1234", cliente1)
conta_corrente = ContaCorrente("4321", cliente1)
conta_poupanca = ContaPoupanca("8524", cliente1)

# conta1.depositar(500)
# conta1.depositar(250)
# conta1.sacar(250)
# conta1.sacar(300)
# conta1.sacar(300)
# conta1.obter_extrato()

# conta_corrente.depositar(500)
# conta_corrente.sacar(0)
# conta_corrente.sacar(250)
# conta_corrente.sacar(150)
# conta_corrente.obter_extrato()

conta_poupanca.obter_extrato()
conta_poupanca.depositar(5000)
# conta_poupanca.sacar(500)
conta_poupanca.sacar(3500)
conta_poupanca.obter_extrato()



# print(conta1.extrato)


