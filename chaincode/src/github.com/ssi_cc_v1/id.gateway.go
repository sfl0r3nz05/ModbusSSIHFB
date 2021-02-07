package main

import (
	"fmt"
	"encoding/json"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) createIDRegistry(stub shim.ChaincodeStubInterface, did string, identity Identity) (string, error) {
	bytes, err := stub.GetState(did)

	if bytes != nil {
		fmt.Printf("Error starting Simple chaincode: %s", bytes)
	}
	idBytes, err := json.Marshal(identity)
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}

	err = stub.PutState(did, idBytes)
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}

	return "", nil
}