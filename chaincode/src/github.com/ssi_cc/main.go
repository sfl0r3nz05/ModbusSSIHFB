package main

import (
	"encoding/json"
	log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	sc "github.com/hyperledger/fabric/protos/peer"
)

type Chaincode struct {
}

const logLevel string = "DEBUG"

// CHANNEL_ENV
var CHANNEL_ENV string

func (cc *Chaincode) Init(stub shim.ChaincodeStubInterface) sc.Response {
	log.Init("DEBUG")
	CHANNEL_ENV = stub.GetChannelID()

	log.Infof("[%s][IdentityCC][Init] Initializing identity root", CHANNEL_ENV)
	idReq := IdentityRequest{}
	_, args := stub.GetFunctionAndParameters()

	err := json.Unmarshal([]byte(args[0]), &idReq)
	if err != nil {
		log.Errorf("[%s][IdentityGateway][CreateIdentity] Error parsing: %v", CHANNEL_ENV, err.Error())
	}

	identityStore := Identity{PublicKey: idReq.PublicKey, Controller: idReq.Controller}
	_, err = cc.createIDRegistry(stub, idReq.Did, identityStore)
	if err != nil {
		log.Errorf("[%s][IdentityGateway][CreateIdentity] Error parsing: %v", CHANNEL_ENV, err.Error())
		return shim.Error(err.Error())
	}
	log.Infof("[%s][IdentityCC][Init] Chaincode initialized", CHANNEL_ENV)

	return shim.Success(nil)
}

// Invoke is called as a result of an application request to run the chaincode.
func (cc *Chaincode) Invoke(stub shim.ChaincodeStubInterface) sc.Response {
	log.Init("DEBUG")
	fcn, params := stub.GetFunctionAndParameters()
	var err error
	var result string
	CHANNEL_ENV = stub.GetChannelID()
	if fcn == "proxy" {
		result, err = cc.verifyArgs(stub, params)
	}
	if err != nil {
		log.Errorf("[%s][IdentityCC][Init] Errror %v", CHANNEL_ENV, err)
		return shim.Error(err.Error())
	}
	return shim.Success([]byte(result))
}

func main() {
	err := shim.Start(new(Chaincode))
	if err != nil {
		panic(err)
	}
}
