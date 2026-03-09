import streamlit as st

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
      return True, f"R${valor:.2f} Depositado com sucesso!"
    except ValueError as e:
      return False, str(e)

  def sacar(self, valor):
    try:
      if valor <= 0:
        raise ValueError("Valor inválido: deve ser maior que zero!")
       
      if self.__saldo < valor:
        raise ValueError("Saldo insuficiente!")
    
      self.saldo -= valor
      self.extrato.append(f"Saque - R${valor:.2f}")
      return True, f"R${valor:.2f} sacado com sucesso!"
    except ValueError as e:
      return False, str(e)

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
        if novo_valor <= self.limite_especial:
          self.limite_especial -= novo_valor
          self.saldo += novo_valor
        else:
          raise ValueError("Saldo ou Limite Especial insuficiente!")

      self.saldo -= valor
      self.extrato.append(f"Saque - R${valor:.2f}")
      return True, f"Saque de R${valor:.2f} efetuado!"  
    
    except ValueError as e:
      return False, str(e)

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
      return True, f"R${valor:.2f} sacado com sucesso!"
    except ValueError as e:
      return False, str(e)

# ===========================================STREAMLIT=======================================  
st.set_page_config(page_title="OOP Bank", page_icon="🏦")

if "conta" not in st.session_state:
  st.session_state.conta = None

st.title("💵 OOP Bank")

if st.session_state.conta is None:
  st.subheader("Abra sua Conta")
  with st.form("my_form"):
    nome = st.text_input("Nome do Cliente")
    email = st.text_input("Email")
    num_conta = st.text_input("Número da Conta")
    tipo_conta = st.selectbox("Tipo de Conta", ["Conta Corrente", "Conta Poupança"])

    submitted = st.form_submit_button("Criar Conta")
    if submitted:
      if not nome or len(nome) < 3:
        st.warning("Nome precisa ter pelo menos 3 letras.")
      elif not "@" in email:
        st.warning("Email inválido!")
      elif not num_conta:
        st.warning("Número de conta inválido")
      else:
        st.success("Conta criada com sucesso!", icon="✅")
        cliente = Cliente(nome, email)
        if tipo_conta == "Conta Corrente":
          conta = ContaCorrente(num_conta, cliente)
        else:
          conta = ContaPoupanca(num_conta, cliente)
        st.session_state.conta = conta
        st.rerun()

else:
  if "toast" in st.session_state:
    st.toast(st.session_state.toast[0], icon=st.session_state.toast[1])
    del st.session_state.toast
  st.subheader(f"Bem vindo(a), {st.session_state.conta.cliente.nome}")

  tipo = type(st.session_state.conta).__name__
  if tipo == "ContaCorrente":
    st.markdown(f"**Conta Corrente** | Número: {st.session_state.conta.numero}")
    st.markdown(f"Limite Cheque Especial: R${st.session_state.conta.limite_especial:.2f}")
  elif tipo == "ContaPoupanca":
    st.markdown(f"**Conta Poupança** | Número: {st.session_state.conta.numero}")

  st.metric(label="Saldo Atual", value=f"R${st.session_state.conta.saldo:.2f}")
  st.divider()

  col1, col2 = st.columns(2)
  with col1:
    st.subheader("Depósito")
    valor = st.number_input("Valor para depósito", min_value=0.01, step=0.01)
    if st.button("Depositar"):
      sucesso, mensagem = st.session_state.conta.depositar(valor)
      if sucesso:
        st.session_state.toast = (mensagem, "✅")
        st.rerun()
      else:
        st.session_state.toast = (mensagem, "❌")
        st.rerun()

  with col2:
    st.subheader("Saque")
    valor = st.number_input("Valor para saque", min_value=0.01, step=0.01)
    if st.button("Sacar"):
      sucesso, mensagem = st.session_state.conta.sacar(valor)
      if sucesso:
        st.session_state.toast = (mensagem, "✅")
        st.rerun()
      else:
        st.session_state.toast = (mensagem, "❌")
        st.rerun()
  
  st.divider()

  if st.button("Sair/Fechar Conta"):
    st.session_state.conta = None
    st.rerun()





