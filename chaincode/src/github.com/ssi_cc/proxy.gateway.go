package main

import (
	"encoding/json"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) verifyArgs(stub shim.ChaincodeStubInterface, args []string) (string, error) {
	var result string

	result = "10"

	idReq := Request{}
	err := json.Unmarshal([]byte(args[0]), &idReq)

	return result, err
}