package main

import (
	"fmt"
	"encoding/json"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	sc  "github.com/hyperledger/fabric/protos/peer"
)

type Chaincode struct {
}

func (cc *Chaincode) Init(stub shim.ChaincodeStubInterface) sc.Response {

	idReq := IdentityRequest{}
	_, args := stub.GetFunctionAndParameters()

	err := json.Unmarshal([]byte(args[0]), &idReq)
	if err != nil {
		
	}
	identityStore := Identity{PublicKey: idReq.PublicKey, Controller: idReq.Controller}
	_, err = cc.createIDRegistry(stub, idReq.Did, identityStore)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

// Invoke is called as a result of an application request to run the chaincode.
func (cc *Chaincode) Invoke(stub shim.ChaincodeStubInterface) sc.Response {
	fcn, params := stub.GetFunctionAndParameters()
	//var identity *Identity
	var err error
	var result string
	if fcn == "proxy" {
		result, err = cc.verifyArgs(stub, params)
	}
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success([]byte(result))
}

func main() {
	err := shim.Start(new(Chaincode))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}
}
