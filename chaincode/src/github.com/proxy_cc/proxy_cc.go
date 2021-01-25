package main

import (
	log "log"
	"encoding/json"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	sc "github.com/hyperledger/fabric/protos/peer")


// Chaincode struct
type Chaincode struct {
}

// IdentityRequest to serialize args
type IdentityRequest struct {
	Did        string `json:"did"`
	Controller string `json:"controller,omitempty"`
	PublicKey  string `json:"publicKey"`
	Payload    string `json:"payload,omitempty"` // me pasa una firma // el controller lo meto yo
	Access     int    `json:"access,omitempty"`
}

// Identity stored in bc
type Identity struct {
	PublicKey  string `json:"publicKey"`
	Controller string `json:"controller"` // issuer's DID
	Access     int    `json:"access,omitempty"`
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

func (cc *Chaincode) Init(stub shim.ChaincodeStubInterface) sc.Response {
	idReq := IdentityRequest{}
	_, args := stub.GetFunctionAndParameters()

	if len(args) != 3 {
		return shim.Error("Incorrect argument numbers. Expecting 4")
	}

	idReq.Did = args[0]
	idReq.Controller= args[1]
	idReq.PublicKey= args[2]


	identityStore := Identity{PublicKey: idReq.PublicKey, Controller: idReq.Controller, Access: 4}

	idBytes, err := json.Marshal(identityStore)
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(idReq.Did, idBytes)
	if err != nil {
		return shim.Error(err.Error())
	}

	return shim.Success(nil)
}

// Invoke is called as a result of an application request to run the chaincode.
func (cc *Chaincode) Invoke(stub shim.ChaincodeStubInterface) sc.Response {
	function, args := stub.GetFunctionAndParameters()
	var err error
	var result string
	if function == "query" {
		return cc.getIDRegistry(stub, args)
	}
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success([]byte(result))
}

func (cc *Chaincode) getIDRegistry(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	var did string // Entities
	did = args[0]
	idStored := Identity{}
	idBytes, err := stub.GetState(did)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + did + "\"}"
		return shim.Error(jsonResp)
	}
	if idBytes == nil {
		return shim.Error(ERRORnotID)
	}
	err = json.Unmarshal(idBytes, &idStored)
	if err != nil {
		log.Errorf("[%s][%s][getIDRegistry] Error parsing identity: %v", CHANNEL_ENV, IDREGISTRY, err.Error())
		return nil, errors.New(ERRORParsingID + err.Error())
	}
	log.Infof("Get Identity: %s",idBytes)

	return shim.Success(idBytes)
}

func main() {
	err := shim.Start(new(Chaincode))
	if err != nil {
		panic(err)
	}
}
