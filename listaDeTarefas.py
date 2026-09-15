import csv
import os
from datetime import datetime


class Tarefa:
    def __init__(self, descricao, data="Sem data", concluida=False):
        self.descricao = descricao
        self.data = data
        self.concluida = concluida

    def concluir(self):
        self.concluida = True


class GerenciadorTarefas:
    ARQUIVO = "tarefa.csv"

    def __init__(self):
        self.tarefa = []

        if not os.path.exists(self.ARQUIVO):
            with open(self.ARQUIVO, mode="w", newline="") as f:
                escritor = csv.writer(f)
                escritor.writerow(["Descricao", "Data Limite", "Concluida"])

        self.carregar()

    def carregar(self):
        with open(self.ARQUIVO, mode="r", newline="") as f:
            leitor = csv.reader(f)

            for i, linha in enumerate(leitor):
                if i == 0:
                    continue

                if linha:
                    descricao = linha[0]

                    if len(linha) >= 3:
                        data = linha[1]
                        concluida = (linha[2] == "True")
                    else:
                        data = "Sem data"
                        concluida = (linha[1] == "True")

                    self.tarefa.append(
                        Tarefa(descricao, data, concluida)
                    )

    def salvar(self):
        with open(self.ARQUIVO, mode="w", newline="") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Descricao", "Data Limite", "Concluida"])

            for tarefa in self.tarefa:
                escritor.writerow([
                    tarefa.descricao,
                    tarefa.data,
                    tarefa.concluida
                ])

    def adicionar_tarefa(self, descricao, data):
        nova_tarefa = Tarefa(descricao, data)
        self.tarefa.append(nova_tarefa)
        self.salvar()
        print("Tarefa adicionada com sucesso!")

    def listar_tarefas(self):
        if not self.tarefa:
            print("Nenhuma tarefa cadastrada.")
            return

        print("\n--- PENDENTES ---")
        tem_pendente = False

        for i, tarefa in enumerate(self.tarefa):
            if not tarefa.concluida:
                print(
                    f"{i + 1} - {tarefa.descricao} "
                    f"| Data limite: {tarefa.data}"
                )
                tem_pendente = True

        if not tem_pendente:
            print("Nenhuma tarefa pendente.")

        print("\n--- CONCLUÍDAS ---")
        tem_concluida = False

        for i, tarefa in enumerate(self.tarefa):
            if tarefa.concluida:
                print(
                    f"{i + 1} - {tarefa.descricao} "
                    f"| Data limite: {tarefa.data}"
                )
                tem_concluida = True

        if not tem_concluida:
            print("Nenhuma tarefa concluída ainda.")

    def marcar_concluida(self, indice):
        if indice < 0 or indice >= len(self.tarefa):
            print("Número de tarefa inválido.")
            return

        tarefa = self.tarefa[indice]
        tarefa.concluir()
        self.salvar()

        print(
            f'Tarefa "{tarefa.descricao}" '
            f'(Data limite: {tarefa.data}) marcada como concluída!'
        )

    def remover_tarefa(self, indice):
        if indice < 0 or indice >= len(self.tarefa):
            print("Número de tarefa inválido.")
            return

        tarefa_removida = self.tarefa.pop(indice)
        self.salvar()

        print(
            f'Tarefa "{tarefa_removida.descricao}" '
            f'(Data limite: {tarefa_removida.data}) removida com sucesso!'
        )


def menu():
    gerenciador = GerenciadorTarefas()

    while True:
        print("\n--- MENU TODO LIST ---")
        print("1 - Adicionar Tarefa")
        print("2 - Listar Tarefas")
        print("3 - Marcar Tarefa como Concluída")
        print("4 - Remover Tarefa")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            descricao = input("Descrição da tarefa: ")

            while True:
                data = input(
                    "Data Limite da tarefa (dd/mm/aaaa): "
                )

                try:
                    datetime.strptime(data, "%d/%m/%Y")
                    break

                except ValueError:
                    print(
                        "Data inválida! "
                        "Digite no formato dd/mm/aaaa."
                    )

            gerenciador.adicionar_tarefa(descricao, data)

        elif opcao == "2":
            gerenciador.listar_tarefas()

        elif opcao == "3":
            gerenciador.listar_tarefas()

            try:
                numero = int(
                    input(
                        "Número da tarefa a marcar como concluída: "
                    )
                )
                gerenciador.marcar_concluida(numero - 1)

            except ValueError:
                print("Digite um número válido.")

        elif opcao == "4":
            gerenciador.listar_tarefas()

            try:
                numero = int(
                    input("Número da tarefa a remover: ")
                )
                gerenciador.remover_tarefa(numero - 1)

            except ValueError:
                print("Digite um número válido.")

        elif opcao == "5":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()