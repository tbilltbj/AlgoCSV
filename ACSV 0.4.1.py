#----------#        IMPORTS
import requests
import json
import csv
import datetime

#----------#        GLOBAL VAR
txnOrder = []
txnDB = {}
groupDB = {}
asaFetchList = []

try:
    inFile = open('asaDB.json', 'r')
    asaDB = json.load(inFile)
    inFile.close()
    print('loaded asaDB')
except IOError:
    asaDB = {}
    print('fresh asaDB')

try:
    inFile = open('wallet.txt', 'r')
    wallet = inFile.read()
    inFile.close()
except IOError:
    wallet = str(input('Paste wallet ID and press Enter: '))



#----------#        CONTACTS
yieldlyDB = {'FMBXOFAQCSAD4UWU4Q7IX5AV4FRV6AKURJQYGXLW3CTPTQ7XBX6MALMSPY'   :   'Yieldly - YLDY-YLDY/ALGO',
             'VUY44SYOFFJE3ZIDEMA6PT34J3FAZUAE6VVTOTUJ5LZ343V6WZ3ZJQTCD4'   :   'Yieldly - YLDY-OPUL',
             'U3RJ4NNSASBOIY25KAVVFV6CFDOS22L7YLZBENMIVVVFEWT5WE5GHXH5VQ'   :   'Yieldly - GEMS-GEMS',
             'BXLXRYBOM7ZNYSCRLWG6THNMO6HASTIRMJGSNJANZFS6EB3X4JY2FZCJNA'   :   'Yieldly - YLDY-GEMS',
             'AAXO2CVK6SHKHNROZZH3435UAYMQXZP4UTLO5LQCNTDZAXEGJJ2OPHFX54'   :   'Yieldly - YLDY-ARCC',
             '4UPQ2HSD7O6WY3HP33JXMPGYNMV56U3YK5WT6CTSBLGS466JPOFUVCCSTA'   :   'Yieldly - ARCC-ARCC',
             'YCHXDWES2VJDEKAHWPC344N6WK3FQOZL5VIZYMCDHDIUTTUZPC4IA6DEZY'   :   'Yieldly - YLDY-CHOICE',
             'KDZS6OV5PAARFJPRZYRRQWCZOCPICB6NJ4YNHZKNCNKIVOLSL5ZCPMY24I'   :   'Yieldly - YLDY-SMILE',
             '55CUF2LA45PJWIUK2KZOGN54N2POJHXAWTSVGR5HFSO4JUUDJ3SOURUVGQ'   :   'Yieldly - SMILE-SMILE',
             'IR2HQCMN6GPTKGCTR54YXFFUBB4A7FRZR76U2BJAS4XBLNJHZX7RMOPBIQ'   :   'Yieldly - YLDY-XET',
             'GLHS7QEDDSQVHNTOVFELY3ISMB44TL7I7RQ36BNFW7KMJEZA4SQUFJHV6E'   :   'Yieldly - CHOICE-CHOICE',
             '2RQGRKUSDCZAEFFCXXCQBCVH6KOR7FZW6N3G7B547DIS76AGQJAZZVPPPY'   :   'Yieldly - OPUL-OPUL',
             '3OZ3HAIID3NPKB5N3B6TGFUBX44ZBZDNNRWGY6HSPQLP3NRSQW7D6ZKFEY'   :   'Yieldly - XET-XET',
             'ZMJVS7F3DXYDE6XIBXGWLEL6VXUYLCN4HTOW57QDLZ2TAMOWZK7EIYAQF4'   :   'Yieldly - YLDY-AKITA',
             '233725844' :  'Yieldly',
             '233725848' :  'Yieldly',
             '233725850' :  'Yieldly - YLDY-YLDY/ALGO',
             '348079765' :  'Yieldly - YLDY-OPUL',
             '419301793' :  'Yieldly - GEMS-GEMS',
             '393388133' :  'Yieldly - YLDY-GEMS',
             '385089192' :  'Yieldly - YLDY-ARCC',
             '498747685' :  'Yieldly - ARCC/ARCC',
             '447336112' :  'Yieldly - YLDY-CHOICE',
             '352116819' :  'Yieldly - YLDY-SMILE',
             '373819681' :  'Yieldly - SMILE-SMILE',
             '424101057' :  'Yieldly - YLDY-XET',
             '464365150' :  'Yieldly - CHOICE-CHOICE',
             '367431051' :  'Yieldly - OPUL-OPUL',
             '470390215' :  'Yieldly - XET-XET',
             '511597182' :  'Yieldly - YLDY-AKITA',
             '511593477' :  'Yieldly - (AKITA/ALGO)LP-YLDY'}

algofiDB = {'3EPGHSNBBN5M2LD6V7A63EHZQQLATVQHDBYJQIZ6BLCBTIXA5XR7ZOZEB4'   :   'Algofi - Creator',
            '2SGUKZCOBEVGN3HPKSXPS6DTCXZ7LSP6G3BQF6KVUIUREBBY2QTGSON7WQ'   :   'Algofi - Manager',
            'TY5N6G67JWHSMWFFFZ252FXWKLRO5UZLBEJ4LGV7TPR5PVSKPLDWH3YRXU'   :   'Algofi - ALGO Market',
            'ABQHZLNGGPWWZVA5SOQO3HBEECVJSE3OHYLKACOTC7TC4BS52ZHREPF7QY'   :   'Algofi - USDC Market',
            'W5UCMHDSTGKWBOV6YVLDVPJGPE4L4ISTU6TGXC7WRF63Y7GOVFOBUNJB5Q'   :   'Algofi - goBTC Market',
            'KATD43XBJJIDXB3U5UCPIFUDU3CZ3YQNVWA5PDDMZVGKSR4E3QWPJX67CY'   :   'Algofi - goETH Market',
            'OPY7XNB5LVMECF3PHJGQV2U33LZPM5FBUXA3JJPHANAG5B7GEYUPZJVYRE'   :   'Algofi - STBL Market',
            'DYLJJES76YQCOUK6D4RALIPJ76U5QT7L6A2KP6QTOH63OBLFKLTER2J6IA'   :   'Algofi - STBL Staking',
            'Z3GWRL5HGCJQYIXP4MINCRWCKWDHZ5VSYJHDLIDLEIOARIZWJX6GLAWWEI'   :   'Algofi - STBL/USDC LP Staking',
            '465818260' :  'Algofi - Manager',
            '465814065' :  'Algofi - ALGO Market',
            '465814103' :  'Algofi - USDC Market',
            '465814149' :  'Algofi - goBTC Market',
            '465814222' :  'Algofi - goETH Market',
            '465814278' :  'Algofi - STBL Market',
            '482625868' :  'Algofi - STBL Staking',
            '485247444' :  'Algofi - STBL/USDC LP Staking'}

tinyDB = {}
      
#----------#        GET TXNs
print('getting wallet transactions')
##txn limit is 1000 by default. 0 no longer removes limit in testing
#Type = transaction type. tInQ = quantity in. tInId, Incoming asset ID. same for out and fee.
#Wallet will be walletShort var.
#Platform will be Wallet/Yieldly/Tinyman. Where ever assets are located or swaped.
#ID = transaction ID.
#GroupID = '' if no group. otherwise group ID.
#Date = date stored in UNIX time, convert.

def saveTxn(Type, InQ, InID, OutQ, OutID, Fee, Wallet, Platform, ID, GroupID, Date):
    #add txnID to txnOrder list. use to build rows in oldest > newest order
    txnOrder.insert(0, ID)
    transaction = {'type'   :   Type,
                   'inQ'    :   InQ,
                   'inID'   :   InID,
                   'outQ'   :   OutQ,
                   'outID'  :   OutID,
                   'fee'    :   Fee,
                   'wallet' :   Wallet,
                   'platform':  Platform,
                   'id'     :   str(ID),
                   'group'  :   str(GroupID),
                   'date'   :   Date}
    txnDB.update({ID : transaction})

def tinyDBAdd(sender, receiver):
    if sender not in tinyDB and sender != wallet:
        tinyDB.update({sender : 'Tinyman'})
    elif receiver not in tinyDB and receiver != wallet:
        tinyDB.update({receiver : 'Tinyman'})

def processTXNS(getTxn):
    if getTxn['id'] in txnOrder: pass
    else:
    
        #Fresh txn. 
        tType = ''
        tInQ = 0
        tInID = ''
        tOutQ = 0
        tOutID = ''
        tFee = 0
        tPlatform = ''
        tID = ''
        tGroupID = ''
        tDate = ''
        
        #Base definitions
        tSender = str(getTxn['sender'])
        tID = getTxn['id']
        tDate = str(datetime.datetime.fromtimestamp(getTxn['round-time']))

        #Group ID
        if 'group' in getTxn: tGroupID = getTxn['group']
        else: tGroupID = ''
        #Algo Txn Fees
        if getTxn['sender'] == wallet: tFee = getTxn['fee']
        else: tFee = 0

        #use TXN type to find correct transaction details
        #TX TYPES
        if getTxn['tx-type'] == 'pay':          #ALGO TXN
            txnDetails = getTxn['payment-transaction']
            tReceiver = txnDetails['receiver']
            if txnDetails['amount'] != 0: #0 ALGO TXNS are common for compounding rewards
                if tReceiver == wallet:
                    tType = 'Receive'
                    tInQ = txnDetails['amount']
                    tInID = 'ALGO'
                else:
                    tType = 'Send'
                    tOutQ = txnDetails['amount']
                    tOutID = 'ALGO'
            elif tSender == wallet and tReceiver == wallet: #0 ALGO network activity to receive rewards
                tType = 'Staking'

        elif getTxn['tx-type'] == 'axfer':      #ASA TXN
            txnDetails = getTxn['asset-transfer-transaction']
            tAsset = str(txnDetails['asset-id'])
            tReceiver = txnDetails['receiver']
            if 'close-to' in txnDetails: #Remove ASA
                tType = 'Close Asa'
                tOutID = tAsset
                tPlatform = tAsset
            elif tSender == wallet:
                if tReceiver == wallet: #usually means Sign for ASA
                    tType = 'Sign for Asa'
                    tInId = tAsset
                    tPlatform = tAsset
                elif tReceiver is not wallet: #send ASA
                    tType = 'Send'
                    tOutQ = txnDetails['amount']
                    tOutID = tAsset
            elif tSender is not wallet and tReceiver == wallet: #receive ASA
                tType = 'Receive'
                tInQ = txnDetails['amount']
                tInID = tAsset


                
            
        elif getTxn['tx-type'] == 'appl':
            txnDetails = getTxn['application-transaction']
            tReceiver = str(txnDetails['application-id'])
            if 'application-args' in txnDetails:
                #1st app arguement defines Tinyman actions
                #These are GROUP definitions. for use in row building
                #the first txn of a group does not contain defining info
                appArg = txnDetails['application-args']
                if appArg != []:
                    if appArg[0] == 'Ym9vdHN0cmFw':
                        groupDB[tGroupID] = 'Begin pool'
                        tinyDBAdd(tReceiver, tSender)
                    elif appArg[0] == 'c3dhcA==':
                        tinyDBAdd(tReceiver, tSender)
                        if appArg[1] == 'Zmk=': groupDB[tGroupID] = 'sellTrade'
                        elif appArg[1] ==  'Zm8=': groupDB[tGroupID] = 'buyTrade'
                    elif appArg[0] == 'bWludA==':
                        groupDB[tGroupID] = 'Add to pool'
                        tinyDBAdd(tReceiver, tSender)
                    elif appArg[0] == 'YnVybg==':
                        groupDB[tGroupID] = 'Remove from pool'
                        tinyDBAdd(tReceiver, tSender)
                    elif appArg[0] == 'cmVkZWVt':
                        groupDB[tGroupID] = 'Redeem slippage'
                        tinyDBAdd(tReceiver, tSender)
                    #else: groupDB[tGroupID] = 'unknown'
                elif txnDetails['on-completion'] == 'optin': tType = 'App opt in'
                else: groupDB[tGroupID] = 'unknown0'
            else: groupDB[tGroupID] = 'unknown1'

            if 'inner-txns' in getTxn:
                innerIDCut = tID.zfill(4)
                innerID = innerIDCut[:4] + '...inner-txn...' + innerIDCut[-4:]
                innerTxnList = getTxn['inner-txns']
                for innerTxn in innerTxnList:
                    if innerTxn['tx-type'] == 'pay':
                        innerDetails = innerTxn['payment-transaction']
                        innerAsset = 'ALGO'
                    elif innerTxn['tx-type'] == 'axfer':
                        innerDetails = innerTxn['asset-transfer-transaction']
                        innerAsset = innerDetails['asset-id']
                    if innerDetails['receiver'] == wallet:
                        saveTxn('inner txn', innerDetails['amount'], innerAsset, 0, '', 0, walletShort, tPlatform, innerID, tGroupID, tDate)
                    elif innerTxn['sender'] == wallet:
                        saveTxn('inner txn', 0, '', innerDetails['amount'], innerAsset, 0, walletShort, tPlatform, innerID, tGroupID, tDate)
                        
        
        #Handle TXN rewards
        if tSender == wallet and getTxn['sender-rewards'] > 0:
            saveTxn('Staking', getTxn['sender-rewards'], 'ALGO', 0, '', 0, walletShort, 'Participation Rewards', str(tID + '/reward'), tGroupID, tDate) 
        elif tReceiver == wallet and getTxn['receiver-rewards'] > 0:
            saveTxn('Staking', getTxn['receiver-rewards'], 'ALGO', 0, '', 0, walletShort, 'Participation Rewards', str(tID + '/reward'), tGroupID, tDate)
        
        #add ASA ID to DB for later use
        if getTxn['tx-type'] == 'axfer'and str(txnDetails['asset-id']) not in asaDB and str(txnDetails['asset-id']) not in asaFetchList:
            asaFetchList.append(str(txnDetails['asset-id']))

        #Check contacts      
        if tSender in yieldlyDB or tReceiver in yieldlyDB:
            tPlatform = 'Yieldly'
        elif tSender in algofiDB or tReceiver in algofiDB:
            tPlatform = 'Algofi'
        elif tSender in tinyDB or tReceiver in tinyDB:
            tPlatform = 'Tinyman'

        #Save TXN entry
        saveTxn(tType, tInQ, tInID, tOutQ, tOutID, tFee, walletShort, tPlatform, tID, tGroupID, tDate)


txnResponse = requests.get('https://algoindexer.algoexplorerapi.io/v2/accounts/'
                           + wallet + '/transactions', params={"limit": 10000})
walletNameCut = wallet.zfill(6)
walletShort = walletNameCut[:6] + '...' + walletNameCut[-6:]
txnCount = 0    
txnJson = txnResponse.json()

for getTxn in txnJson['transactions']:
    txnCount += 1
    processTXNS(getTxn)

while 'next-token' in txnJson:
    txnResponse = requests.get('https://algoindexer.algoexplorerapi.io/v2/accounts/'
                               + wallet + '/transactions', params={'next': txnJson['next-token'], "limit": 10000})
    txnJson = txnResponse.json()
    for nGetTxn in txnJson['transactions']:
        txnCount += 1
        processTXNS(nGetTxn)

print('rows found: ', txnCount)

#----------#        GET ASA
def getAsa(asaID):
    #get asa response
    asaResponse = requests.get('https://algoindexer.algoexplorerapi.io/v2/assets/' + str(asaID))
    asaJSON = asaResponse.json()
    #set required details to vars
    asaDetails = asaJSON['asset']
    asaParams = asaDetails['params']
    if asaParams['unit-name'] == 'TM1POOL':
        asaPoolTick = asaParams['name']
        asaPoolTickCut = asaPoolTick.zfill(12)
        asaTick = 'TM1POOL -' + asaPoolTickCut[12:]
    else:
        asaTick = asaParams['unit-name'] + '-ASA'
    #build asa dictionary entry
    details = {"id"         : asaID,
               "name"       : asaParams['name'],
               "ticker"     : asaTick,
               "decimals"   : asaParams['decimals']}
    #return asa dictionary entry
    return details
#print('skipping asaDB for now')
#####for asaID within the list to check, pass to check function and store returned dictionary
print('\nfinding ' + str(len(asaFetchList)) + ' ASA details')
for asaID in asaFetchList:
    if asaID in asaDB:
        print('loaded ASA ID: ', str(asaID))
    else:
        print('getting ASA ID: ', str(asaID))
        asaDB.update({asaID: getAsa(str(asaID))})

#----------#        Row Building
def assetQ(asaID, baseQ):
    if asaID != 'ALGO':
        asaDetails = asaDB[str(asaID)]
        decimal = asaDetails['decimals']
    else: decimal = 6

    if decimal == 0:
        return baseQ
    else:
        qString = str(baseQ)
        qStringFilled = qString.zfill(decimal)
        return qStringFilled[:-decimal] + '.' + qStringFilled[-decimal:]
    


    
def writeRow(Type, InQ, InID, OutQ, OutID, Fee, Wallet, Platform, ID, GroupID, Date):
    if Type == 'Sign for Asa' and Platform in asaDB:
        asaDetails = asaDB[Platform]
        Platform = asaDetails['name']
    elif Type == 'Close Asa' and Platform in asaDB:
        asaDetails = asaDB[Platform]
        Platform = asaDetails['name']
    elif Type == 'buyTrade': Type = 'Trade'
    elif Type == 'sellTrade': Type = 'Trade'

    #Prepare incoming
    if InQ == 0: InQ = '' 
    if InID != '':
        if InQ != '': InQ = assetQ(InID, InQ)
        if InID != 'ALGO':
            asaDetails = asaDB[str(InID)]
            InID = asaDetails['ticker']       
    #Prepare outgoing
    if OutQ == 0: OutQ = ''
    if OutID != '':
        if OutQ != '': OutQ = assetQ(OutID, OutQ)
        if OutID != 'ALGO':
            asaDetails = asaDB[str(OutID)]
            OutID = asaDetails['ticker']
    #Prepare fees
    if Fee == 0:
        Fee = ''
        FeeID = ''
    elif Fee != 0:
        Fee = assetQ('ALGO', Fee)
        FeeID = 'ALGO'

    
    
    row = (Type, InQ, InID, OutQ, OutID, Fee, FeeID, Wallet, Platform, ID, GroupID, Date)
    writer.writerow(row)
    
rowGroup = ''
txnCount = 0
gType = ''
gType = ''
gInQ = 0
gInID = ''
gOutQ = 0
gOutID = ''
gFee = 0
gWallet = walletShort
gPlatform = ''
gID = ''
gGroupID = ''
gDate = ''

print('Begin Row Building\n')

algocsv = open('ALGO.csv', 'w', newline='')
writer = csv.writer(algocsv)
row = ['Type', 'In Quantity', 'In ID',
       'Out Quantity', 'Out ID',
       'Fee Quantity', 'Fee ID',
       'Wallet', 'Platform',
       'ID', 'Group ID', 'Date']
writer.writerow(row)

for txnID in txnOrder:
    txnDetails = txnDB[txnID]
    rType = txnDetails['type']
    rInQ = txnDetails['inQ']
    rInID = txnDetails['inID']
    rOutQ = txnDetails['outQ']
    rOutID = txnDetails['outID']
    rFee = txnDetails['fee']
    rWallet = walletShort
    rPlatform = txnDetails['platform']
    rID = str(txnDetails['id'])
    rGroupID = str(txnDetails['group'])
    rDate = txnDetails['date']

    #GROUPS
    if rGroupID != '' and rType != 'Staking':
        if rGroupID != rowGroup and rowGroup != '':
            #TXN group is different from last
            #Save row and clear gVars
            writeRow(gType, gInQ, gInID, gOutQ, gOutID, gFee, gWallet, gPlatform, 'TXN Count: ' + str(txnCount), gGroupID, gDate)
            gType = ''
            gInQ = 0
            gInID = ''
            gOutQ = 0
            gOutID = ''
            gFee = 0
            gWallet = walletShort
            gPlatform = ''
            gID = ''
            gGroupID = ''
            gDate = ''
            txnCount = 0

        #Start working group row
        txnCount += 1
        rowGroup = rGroupID
        if rowGroup in groupDB: gType = groupDB[rowGroup]
        if gType == '' and rType != '': gType = rType
        if gPlatform == '' and rPlatform != '': gPlatform = rPlatform
        if gDate == '': gDate = rDate
        if gGroupID == '': gGroupID = rGroupID

        #Add Row Fees
        gFee += rFee

        #Group Types  --  Tinyman v1
        if gType == 'Begin pool':
            if txnCount == 1: gFee += rOutQ #Fee to tinyman to create pool and opt into assets
            else: pass #remaining txns in group are not needed
        elif gType == 'sellTrade':
            if txnCount == 1: gFee += rOutQ #Fees to tinyman to operate app
            elif txnCount == 2: pass #Tinyman App Call
            elif txnCount == 3: #Send asset for trade
                gOutQ = rOutQ
                gOutID = rOutID
            elif txnCount == 4: #Receive asset from trade
                gInQ = rInQ
                gInID = rInID
                swapFee = int(((gInQ * 100)/99.7) - gInQ)
                writeRow('Trade Fee', 0, '', swapFee, rInID, 0, gWallet, gPlatform, '0.3% of Received Asset', rGroupID, gDate)
        elif gType == 'buyTrade':
            if txnCount == 1: gFee += rOutQ #Fees to tinyman to operate app
            elif txnCount == 2: pass #Tinyman App Call
            elif txnCount == 3: #Send asset for trade
                gOutQ = rOutQ
                gOutID = rOutID
                swapFee = int(gOutQ - (gOutQ * 0.997))
                writeRow('Trade Fee', 0, '', swapFee, rOutID, 0, gWallet, gPlatform, '0.3% of Sent Asset', rGroupID, gDate)
            elif txnCount == 4: #Receive asset from trade
                gInQ = rInQ
                gInID = rInID
        elif gType == 'Add to pool':
            if txnCount == 1: gFee += rOutQ #Fee to tinyman to operate app
            elif txnCount == 2: pass
            elif txnCount == 3: #Add 1st asset to pool. Seperate row as cant send two on one row
                writeRow(gType, 0, '', rOutQ, rOutID, '', gWallet, gPlatform, 'Extra Txn', rGroupID, gDate)
            elif txnCount == 4: #Add 2nd asset to pool. Add to group row
                gOutQ = rOutQ
                gOutID = rOutID
            elif txnCount == 5: #Receive Pool tokens to redeem value later.
                gInQ = rInQ
                gInID = rInID
        elif gType == 'Remove from pool':
            if txnCount == 1: gFee += rOutQ #Fee to tinyman to operate app
            elif txnCount == 2: pass
            elif txnCount == 3: #Get 1st asset from pool. Seperate row as cant send two on one row
                writeRow(gType, rInQ, rInID, 0, '', '', gWallet, gPlatform, 'Extra Txn', rGroupID, gDate)
            elif txnCount == 4: #Get 2nd asset from pool. Add to group row
                gInQ = rInQ
                gInID = rInID
            elif txnCount == 5: #Send tokens to pool for returned assets.
                gOutQ = rOutQ
                gOutID = rOutID
        elif gType == 'Redeem slippage':
            gInQ = rInQ
            gInID = rInID
            
        else:       #Generic group
            if rInQ != 0: #Incoming asset
                if gInID == '':  #Add asset to group row if empty
                    gInQ = rInQ
                    gInID = rInID
                else:           #new row for additional asset received in this group
                    writeRow(gType, rInQ, rInID, 0, '', '', gWallet, gPlatform, 'Extra Txn', gGroupID, gDate)
            if rOutQ != 0: #Outgoing asset
                if gOutID == '': #Add asset to group row if empty
                    gOutQ = rOutQ
                    gOutID = rOutID
                else:           #new row for additional asset sent in this group
                    writeRow(gType, 0, '', rOutQ, rOutID, '', gWallet, gPlatform, 'Extra Txn', gGroupID, gDate)

    #Single row txn. Pass to write function.    
    elif rGroupID == '' and rType != 'Staking':
        #if rowGroup != '':
        #    writeRow(gType, gInQ, gInID, gOutQ, gOutID, gFee, gWallet, gPlatform, gID, gGroupID, gDate)
        writeRow(rType, rInQ, rInID, rOutQ, rOutID, rFee, rWallet, rPlatform, rID, rGroupID, rDate)

    elif rType == 'Staking':
        writeRow(rType, rInQ, rInID, rOutQ, rOutID, rFee, rWallet, rPlatform, rID, '', rDate)

algocsv.close()

asaDBJson = json.dumps(asaDB)
asaDBFile = open('asaDB.json', 'w')
asaDBFile.write(asaDBJson)
asaDBFile.close()

walletFile = open('wallet.txt', 'w')
walletFile.write(wallet)
walletFile.close()

print('Job Done')
