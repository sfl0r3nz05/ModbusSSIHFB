package main

import (
	"fmt"
	"encoding/json"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	sc  "github.com/hyperledger/fabric/protos/peer")

// Chaincode example simple Chaincode implementation
type Chaincode struct {
}

// Identity stored in bc
type Identity struct {
	PublicKey  string `json:"publicKey"`
	Controller string `json:"controller"` // issuer's DID
}

// Error responses
const (
	ERRORWrongNumberArgs  = `Wrong number of arguments. Expecting a JSON with token information.`
	ERRORParsingData      = `Error parsing data `
	ERRORPutState         = `Failed to store data in the ledger.	`
	ERRORGetState         = `Failed to get data from the ledger. `
	ERRORDelState         = `Failed to delete data from the ledger. `
	ERRORChaincodeCall    = `Error calling chaincode`
	ERRORGetService       = `Error getting service`
	ERRORUpdService       = `Error updating service`
	ERRORServiceNotExists = `Error The service doesn't exist`
	ERRORCreatingService  = "Error storing service"
	ERRORParsingService   = `Error parsing service`
	ERRORServiceExists    = `The service already exists in registry`
	ERRORDidMissing       = `Error calling service, no service DID Specified`
	ERRORStoringIdentity  = `Error storing identity`
	ERRORUpdatingID       = `Error updating identity in ledger`
	ERRORGetID            = `Error getting identity`
	ERRORVerID            = `Error verification unauthorized, the did provided has not access`
	ERRORRevID            = `Error revocation unauthorized, the did provided has not access`
	ERRORVerSign          = `Error verifying signature`
	ERRORRevSign          = `Error revoking signature`
	ERRORRevoke           = `Error revoking Unauthorized, the did provided cannot revoke the identity`
	ERRORnotID            = `Error the identity does not exist`
	ERRORParsingID        = `Error parsing identity`
	ERRORRevokeLedger     = `Error deleting from ledger`
	ERRORIDExists         = `Error the identity already exists`
	ERRORUserAccess       = `Error user has not access`
	ERRORParseJWS         = `Error parsing into JWS`
	ERRORParseX509        = `Error parsing into X509`
	ERRORBase64           = `Error decoding into base64`
	ERRORVerifying        = `Error verifying signature `
	IDGATEWAY             = `ID Gateway`
	IDREGISTRY            = `ID Registry`
	ServiceGATEWAY        = `ID Service Gateway`
	ServiceREGISTRY       = `ID Service Registry`
	JoseUTIL              = `JOSE Util`
)

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
	identity.PublicKey = publicKey
	identity.Controller = controller
	jsonAsBytes, _ := json.Marshal(identity)

	err = stub.PutState(did, jsonAsBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

func (t *Chaincode) Invoke(stub shim.ChaincodeStubInterface) sc .Response {
	fmt.Println("Invoke")
	function, args := stub.GetFunctionAndParameters()
	if function == "setIdRegistry" {
		return t.setIdRegistry(stub, args)
	} else if function == "getIdRegistry" {
		return t.getIdRegistry(stub, args)
	}
	return shim.Error("Invalid invoke function name. Expecting \"setIDRegistry\" \"getIDRegistry\"")
}

func (t *Chaincode) setIdRegistry(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var err error
	var did string
	var publicKey string
	var identity Identity
	var controller string

	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments. Expecting 3")
	}

	did = args[0]
	controller = args[1]
	publicKey = args[2]
	
	identity.PublicKey = publicKey
	identity.Controller = controller
	jsonAsBytes, _ := json.Marshal(identity) //marshal a marbles index struct with emtpy array of strings to clear the index

	// Write the state to the ledger
	err = stub.PutState(did, jsonAsBytes)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(nil)
}

func (t *Chaincode) getIdRegistry(stub shim.ChaincodeStubInterface, args []string) sc .Response {
	var did string
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to getIdRegistry")
	}

	did = args[0]

	didBytes, err := stub.GetState(did)

	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + did + "\"}"
		return shim.Error(jsonResp)
	}
	if didBytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + did + "\"}"
		return shim.Error(jsonResp)
	}
	jsonResp := "{\"Name\":\"" + did + "\",\"Amount\":\"" + string(didBytes) + "\"}"
	fmt.Printf("getIdRegistry Response:%s\n", jsonResp)

	return shim.Success(didBytes)
}

func main() {
	err := shim.Start(new(Chaincode))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}
}
