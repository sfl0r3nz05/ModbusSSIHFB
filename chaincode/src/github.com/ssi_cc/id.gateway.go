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

func (cc *Chaincode) getIDRegistry(stub shim.ChaincodeStubInterface, did string) (*Identity, error) {
    idStored := Identity{}
    idBytes, err := stub.GetState(did)

    if err != nil {
        fmt.Printf("Error starting Simple chaincode: %s", err)
    }

    if idBytes == nil {
        fmt.Printf("Error starting Simple chaincode: %s", err)
    }

    err = json.Unmarshal(idBytes, &idStored)

    if err != nil {
        fmt.Printf("Error starting Simple chaincode: %s", err)
    }
    return &idStored, nil
}