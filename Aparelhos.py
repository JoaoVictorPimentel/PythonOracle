import cx_Oracle
import Config
import Admin

#Área para login do administrador
usuario = input('Informe seu usuário: ')
senha = input('Informe a senha: ')

if usuario == Admin.username and senha == Admin.password:
    print('ACESSO CONCEDIDO')

    connection = None

    #Conexão com o Oracle
    try:
        connection = cx_Oracle.connect(Config.username, Config.password, Config.dsn, cx_Oracle.SYSDBA)
        print('Você está conectado!')
        print('Versão da database conectada: {}'.format(connection.version))
        print('-' * 50)

        # Funções utilizadas no banco de dados
        funcoes = 'FUNÇÕES DO BANCO DE DADOS'
        print(funcoes.center(50))
        print('1 - REGISTRAR UM NOVO APARELHO')
        print('2 - DELETAR UM APARELHO')
        print('3 - ALTERAR UM DADO')
        print('4 - FILTRAR APARELHOS REGISTRADOS')
        print('-' * 50)

        funcao = (input('Informe qual função deseja realizar no banco de dados: '))

        print('-' * 50)

        if funcao == '1':  #Área onde ocorre os registros
            registros = 'ÁREA DE REGISTROS'
            print(registros.center(50))

            qtdRegistros = int(input('Informe quantos registros você deseja realizar: '))

            for linhas in range(qtdRegistros): #Realiza a quantidade de registros informada acima
                print('{}º Aparelho'.format(linhas + 1))
                modelo = input('Informe o modelo do aparelho: ')
                fabricante = input('Informe sua fabricante: ')
                qtdEstoque = int(input('Informe a quantidade em estoque: '))
                valor = float(input('Informe seu valor: R$'))
                print('O ID do aparelho foi gerado automaticamente!')
                print('*' * 25)

                cursor = connection.cursor()

                sql = ('INSERT INTO sys.APARELHOS(IDAPARELHO, MODELO, FABRICANTE, QTDESTOQUE, VALOR)'
                       'VALUES(aparelhos_seq.nextval, :modelo, :fabricante, :qtdEstoque, :valor)')

                cursor.execute(sql, (modelo, fabricante, qtdEstoque, valor))
                connection.commit()

            print('Os dados informados foram adicionados ao banco de dados!')
        elif funcao == '2': #Área onde ocorre a exclusão de um dado
            deletar = 'ÁREA PARA EXCLUSÃO DE DADOS'
            print(deletar.center(50))

            cursor = connection.cursor()
            cursor.execute('select * from sys.APARELHOS')
            dados = cursor.fetchall()

            print('TABELA COM OS DADOS ATUAIS')

            for linha in dados:  # Mostra os dados atuais inseridos no banco
                print('ID: {} | MODELO: {} | FABRICANTE: {} | QUANTIDADE NO ESTOQUE: {} | VALOR: R${}'.format(linha[0],
                linha[1], linha[2], linha[3], linha[4]))

            qtdDeletes = int(input('Informe a quantidade de aparelhos que deseja remover os dados: '))
            print('*' * 25)

            for linhas in range(qtdDeletes): #Executa as exclusões de acordo com a quantidade indicada acima
                delete = input('Informe o ID do {}º aparelho que terá seus dados deletados:  '.format(linhas + 1))
                print('Você tem certeza que deseja deletar os dados desse aparelho? (SIM/NÃO)')
                confirmacao = input()

                if confirmacao.upper() == 'SIM': #Confirma uma exclusão
                    dados = ('DELETE FROM sys.APARELHOS '
                            ' WHERE IDAPARELHO = :idaparelho ')

                    cursor.execute(dados, {'idaparelho': delete})
                    connection.commit()

                    print('As informações desse aparelho foram removidas do banco de dados!')
                    print('*' * 25)
                elif confirmacao.upper() =='NÃO': #Cancela uma exclusão
                    print('Os dados desse aparelho não foram removidos!')
                else:
                    print('Informe apenas (SIM/NÃO), tente novamente!')
        elif funcao == '3':  # Altera algum dado no banco
            cursor = connection.cursor()
            cursor.execute('select * from sys.APARELHOS')
            dados = cursor.fetchall()

            tabela = 'TABELA'
            print(tabela.center(50))
            for linha in dados:  # Mostra os dados atuais inseridos no banco
                print('ID: {} | MODELO: {} | FABRICANTE: {} | QUANTIDADE NO ESTOQUE: {} | VALOR: R${}'.format(linha[0],
                linha[1], linha[2], linha[3], linha[4]))

            # Área para escolher o dado que vai ser alterado
            print('-' * 50)
            print('M - MODELO')
            print('F - FABRICANTE')
            print('Q - QUANTIDADE NO ESTOQUE')
            print('P - PREÇO')

            update = input('Informe o que deseja atualizar: ')

            if update.upper() == 'M':  # Alteração de nome
                id = input('Informe o id do aparelho que deseja renomear: ')
                novoModelo = input('Digite o novo modelo do aparelho: ')

                dados = (' UPDATE sys.APARELHOS '
                         ' SET MODELO = :novoModelo '
                         ' WHERE IDAPARELHO = :id')

                cursor.execute(dados, (novoModelo, id))
                connection.commit()

                print('O modelo do aparelho foi alterado!')
            elif update.upper() == 'F':  # Alteração da fabricante
                id = input('Informe o id do aparelho que deseja alterar sua fabricante: ')
                novaFabricante = input('Digite a nova fabricante do aparelho: ')

                dados = (' UPDATE sys.APARELHOS '
                         ' SET FABRICANTE = :novaFabricante '
                         ' WHERE IDAPARELHO = :id')

                cursor.execute(dados, (novaFabricante, id))
                connection.commit()

                print('A fabricante do aparelho foi alterada!')
            elif update.upper() == 'Q': # Alteração da fabricante
                id = input('Informe o id do aparelho que deseja alterar sua quantidade de estoque: ')
                novaQtd = input('Digite a nova quantidade em estoque: ')

                dados = (' UPDATE sys.APARELHOS '
                         ' SET QTDESTOQUE = :novaQtd '
                         ' WHERE IDAPARELHO = :id')

                cursor.execute(dados, (novaQtd, id))
                connection.commit()

                print('A quantidade do aparelho em estoque foi alterada!')
            elif update.upper() == 'P':  # Alteração da fabricante
                id = input('Informe o id do aparelho que deseja alterar seu preço: ')
                novoValor = input('Digite o novo preço do aparelho: R$')

                dados = (' UPDATE sys.APARELHOS '
                         ' SET VALOR = :novoValor '
                         ' WHERE IDAPARELHO = :id')

                cursor.execute(dados, (novoValor, id))
                connection.commit()

                print('O valor do aparelho foi alterado!')
            else:
                print('Informe um comando válido!')
        elif funcao == '4': #Área onde ocorre a filtragem de dados
            areaDeFiltro = 'ÁREA DE FILTRAGEM'
            print(areaDeFiltro.center(50))
            print('A - APARELHO ESPECÍFICO')
            print('F - FABRICANTE')
            print('I - ID')
            print('T - ATUAL BANCO DE DADOS COMPLETO')

            filtro = input('Informe o filtro que deseja aplicar: ')

            if filtro.upper() == 'A': #Filtra apenas um aparelho em específico
                filtroModelo = input('Informe o modelo do aparelho que deseja filtrar: ')

                cursor = connection.cursor()
                cursor.execute('select * from sys.APARELHOS WHERE MODELO = :filtro', {'filtro':filtroModelo})
                dados = cursor.fetchall()

                print('-' * 50)
                print('Aparelho encontrado: ')

                for linha in dados:  # Mostra os dados do aparelho escolhido pelo usuário
                    print('ID: {} | MODELO: {} | FABRICANTE: {} | QUANTIDADE NO ESTOQUE: {} | VALOR: R${}'.format(
                        linha[0], linha[1], linha[2], linha[3], linha[4]))
            elif filtro.upper() == 'F': # Filtra aparelhos de acordo com sua fabricante
                filtroFabricante = input('Informe a fabricante:  ')

                cursor = connection.cursor()
                cursor.execute('select * from sys.APARELHOS WHERE FABRICANTE = :filtro', {'filtro':filtroFabricante})
                dados = cursor.fetchall()

                print('-' * 50)
                print('Aparelhos encontrados de acordo com a fabricante:')
                for linha in dados:  # Mostra os dados do aparelho escolhido pelo usuário
                    print('ID: {} | MODELO: {} | FABRICANTE: {} | QUANTIDADE NO ESTOQUE: {} | VALOR: R${}'.format(
                        linha[0], linha[1], linha[2], linha[3], linha[4]))
            elif filtro.upper() == 'I': # Filtra os dados de acordo com o id
                filtroID = input('Informe o ID do aparelho que deseja filtrar: ')

                cursor = connection.cursor()
                cursor.execute('select * from sys.APARELHOS WHERE IDAPARELHO = :filtro', {'filtro':filtroID})
                dados = cursor.fetchall()

                print('-' * 50)
                print('Aparelho encontrado de acordo com o ID:')

                for linha in dados:  # Mostra os dados do aparelho escolhido pelo usuário
                    print('ID: {} | MODELO: {} | FABRICANTE: {} | QUANTIDADE NO ESTOQUE: {} | VALOR: R${}'.format(
                        linha[0], linha[1], linha[2], linha[3], linha[4]))
            elif filtro.upper() == 'T':
                atual = 'DADOS ATUAIS'
                cursor = connection.cursor()
                cursor.execute('select * from sys.APARELHOS')
                dados = cursor.fetchall()

                print(atual.center(50))

                for linha in dados:  # Mostra os dados atuais inseridos no banco
                    print('ID: {} | MODELO: {} | FABRICANTE: {} | QUANTIDADE NO ESTOQUE: {} | VALOR: R${}'.format(
                        linha[0], linha[1], linha[2], linha[3], linha[4]))
            else:
                print('Informe um filtro válido!')
    except cx_Oracle.Error as error: #É executado quando a conexão com o oracle falha
        print('Algo deu errado! Procure seu superior e informe o erro: {}'.format(error))
    finally: #Após tudo ser executado no try ele finaliza a conexão
        if connection:
            connection.close()
elif usuario == Admin.username and senha != Admin.password: #Acontece caso o administrador erre a senha
    print('Senha incorreta, tente novamente!')
else: #Acontece caso a pessoa que esteja tentando logar não seja o administrador
    print('Você não é o administrador! Não possui acesso ao sistema!')