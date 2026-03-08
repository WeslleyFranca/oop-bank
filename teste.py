import app as m

cliente1 = m.Cliente("Weslley", "weslley@gmail.com")

conta1 = m.Conta("1234", cliente1)
conta_corrente = m.ContaCorrente("4321", cliente1)
conta_poupanca = m.ContaPoupanca("8524", cliente1)



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