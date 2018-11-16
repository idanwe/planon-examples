import getpass
from zeep import Client

instanceName = input('Planon instance: ')
baseURL = "https://" + instanceName + ".planoncloud.com/nyx/services/"

username = input('Username: ')
password = getpass.getpass()

token = Client(baseURL + 'PlanonSession?wsdl').service.login(username, password)

# Account and Account Group in Planon to be managed
account = input('Planon Account: ')
group = input('Planon Account Group: ')

# Search for AccountGroup by Id, check the namespace ID using accountgroupClient.namespaces if you experience errors
accountgroupClient = Client(baseURL + 'AccountGroup?wsdl')
groupFilter = accountgroupClient.get_type('ns2:AccountGroupFilter')(accountgroupClient.get_type('ns0:FieldFilter')('PnName', group, 'equals'))
accountGroupId = accountgroupClient.service.find(token, groupFilter)[0]

# Search for Account by Id, check the namespace ID using accountClient.namespaces if you experience errors
accountClient = Client(baseURL + 'Account?wsdl')
accountFilter = accountClient.get_type('ns2:AccountFilter')(accountClient.get_type('ns1:FieldFilter')('Accountname', account, 'equals'))
accountId = accountClient.service.find(token, accountFilter)[0]

# Add link
accountgroupClient.service.connectToAccountGroupAccount(token, accountGroupId, accountId)

# Remove link
accountgroupClient.service.disconnectFromAccountGroupAccount(token, accountGroupId, accountId)