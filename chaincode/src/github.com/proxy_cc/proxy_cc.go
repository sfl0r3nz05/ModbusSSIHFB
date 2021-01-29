package main

import (
	"fmt"
	"encoding/json"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	sc  "github.com/hyperledger/fabric/protos/peer"
)

// Chaincode example simple Chaincode implementation
type Chaincode struct {
}

func (t *Chaincode) Init(stub shim.ChaincodeStubInterface) sc .Response {
	fmt.Println("Init")
	_, args := stub.GetFunctionAndParameters()
	var did string
	var publicKey string
	var controller string
	var identity Identity
	var err error

	if len(args) != 3 {
		return shim.Error("Incorrect argument numbers. Expecting 3")
	}

	did = args[0]
	controller = args[1]
	publicKey = args[2]
	identity.Did = did
	identity.PublicKey = publicKey
	identity.Controller = controller
	jsonAsBytes, _ := json.Marshal(identity)

	err = stub.PutState(identity.Did, jsonAsBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

func (t *Chaincode) Invoke(stub shim.ChaincodeStubInterface) sc .Response {
	fmt.Println("Invoke")
	function, args := stub.GetFunctionAndParameters()
	if function == "controllerRegister" {
		return t.controllerRegister(stub, args)
	} else if function == "controllerGet" {
		return t.controllerGet(stub, args)
	} else if function == "entityRegister" {
		return t.entityRegister(stub, args)
	} else if function == "entityGet" {
		return t.entityGet(stub, args)
	} else if function == "didDocRegister" {
		return t.didDocRegister(stub, args)
	} else if function == "didDocGet" {
		return t.didDocGet(stub, args)
	}
	return shim.Error("Invalid invoke function name. Expecting \"entityRegister\" \"entityGet\" \"controllerRegister\" \"controllerGet\"")
}


func (t *Chaincode) controllerRegister(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var err error
	var did string
	var publicKey string
	var controller Controller

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	did = args[0]
	publicKey = args[1]
	controller.Did = did
	controller.PublicKey = publicKey
	jsonAsBytes, _ := json.Marshal(controller) //marshal a marbles index struct with emtpy array of strings to clear the index

	// Write the state to the ledger
	err = stub.PutState(controller.Did, jsonAsBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

func (t *Chaincode) controllerGet(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var did string
	var err error
	var controller Controller

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to entityGet")
	}

	did = args[0]
	controller.Did = did

	didBytes, err := stub.GetState(controller.Did)

	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + controller.Did + "\"}"
		return shim.Error(jsonResp)
	}
	if didBytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + controller.Did + "\"}"
		return shim.Error(jsonResp)
	}
	jsonResp := "{\"Name\":\"" + controller.Did + "\",\"Amount\":\"" + string(didBytes) + "\"}"
	fmt.Printf("entityGet Response:%s\n", jsonResp)

	return shim.Success(didBytes)
}

func (t *Chaincode) entityRegister(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var err error
	var did string
	var publicKey string
	var controller string
	var identity Identity

	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments. Expecting 3")
	}

	did = args[0]
	controller = args[1]
	publicKey = args[2]
	identity.Did = did
	identity.PublicKey = publicKey
	identity.Controller = controller
	jsonAsBytes, _ := json.Marshal(identity) //marshal a marbles index struct with emtpy array of strings to clear the index

	// Write the state to the ledger
	err = stub.PutState(identity.Did, jsonAsBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

func (t *Chaincode) entityGet(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var did string
	var err error
	var identity Identity

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to entityGet")
	}

	did = args[0]
	identity.Did = did
	didBytes, err := stub.GetState(identity.Did)

	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + identity.Did + "\"}"
		return shim.Error(jsonResp)
	}
	if didBytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + identity.Did + "\"}"
		return shim.Error(jsonResp)
	}
	jsonResp := "{\"Name\":\"" + identity.Did + "\",\"Amount\":\"" + string(didBytes) + "\"}"
	fmt.Printf("entityGet Response:%s\n", jsonResp)

	return shim.Success(didBytes)
}

func (t *Chaincode) didDocRegister(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var err error
	var did string
	var publicKey string
	var payload string
	var controller string
	var diddoc DidDoc

	if len(args) != 4 {
		return shim.Error("Incorrect number of arguments. Expecting 3")
	}

	did = args[0]
	controller = args[1]
	publicKey = args[2]
	payload = args[3]
	diddoc.Did = did
	diddoc.Controller = controller
	diddoc.PublicKey = publicKey
	diddoc.Payload = payload
	jsonAsBytes, _ := json.Marshal(diddoc) //marshal a marbles index struct with emtpy array of strings to clear the index

	// Write the state to the ledger
	err = stub.PutState(diddoc.Did, jsonAsBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

func (t *Chaincode) didDocGet(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var err error
	var did string
	var diddoc DidDoc

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to entityGet")
	}

	did = args[0]
	diddoc.Did = did
	didBytes, err := stub.GetState(diddoc.Did)

	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + diddoc.Did + "\"}"
		return shim.Error(jsonResp)
	}
	if didBytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + diddoc.Did + "\"}"
		return shim.Error(jsonResp)
	}
	jsonResp := "{\"Name\":\"" + diddoc.Did + "\",\"Amount\":\"" + string(didBytes) + "\"}"
	fmt.Printf("entityGet Response:%s\n", jsonResp)

	return shim.Success(didBytes)
}

func main() {
	err := shim.Start(new(Chaincode))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}
}
