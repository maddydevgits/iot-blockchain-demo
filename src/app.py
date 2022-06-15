from flask import Flask, render_template, request
from web3 import Web3,HTTPProvider
import json

def connect_with_blockchain():
    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path='../build/contracts/device.json'
    deployed_contract_address='0x69310B6c9ff6A405EBb64421bCC2f00476eA810C'

    with open(compiled_contract_path) as file:
        contract_json=json.load(file)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=deployed_contract_address,abi=contract_abi)
    return contract,web3

app=Flask(__name__)

@app.route('/')
def displaySensoryData():
    contract,web3=connect_with_blockchain()
    h,t=contract.functions.viewFeed().call()
    print(t)
    data=[]
    for i in range(len(h)):
        dummy=[]
        dummy.append(h[i].decode('utf-8'))
        dummy.append(t[i].decode('utf-8'))
        data.append(dummy)
    l=len(data)
    return render_template('index.html',dashboard_data=data,len=l)

@app.route('/addDevice',methods=['GET'])
def addDevice():
    deviceaddr=request.args.get('mobileno')
    contract,web3=connect_with_blockchain()

    tx_hash=contract.functions.addDevice(deviceaddr).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return ('Device Added')

if __name__=="__main__":
    app.run()
