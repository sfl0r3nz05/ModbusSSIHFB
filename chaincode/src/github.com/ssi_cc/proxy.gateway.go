package main

import (
    "fmt"
	"encoding/json"
    log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) verifyArgs(stub shim.ChaincodeStubInterface, args []string) (string, error) {
    log.Infof("[%s][%s][checkArgs] Get Identity", CHANNEL_ENV, IDGATEWAY)
    var result string

    idReq := Request{}
    err := json.Unmarshal([]byte(args[0]), &idReq)
    
    var publicKey string
    var identity *Identity

    if idReq.PublicKey != "" {
        publicKey = parseKey(idReq.PublicKey)
        params, err := checkSignature(idReq.Payload, publicKey)
        fmt.Printf("params 2: %s", params)
        return result, err
    }

    identity, err = cc.getIDRegistry(stub, idReq.Did)
	if err != nil {
		log.Errorf("[%s][%s][checkArgs] Error verifying signature: %v", CHANNEL_ENV, IDGATEWAY, err.Error())
		return "", err
	}

	publicKey = parseKey(identity.PublicKey)
	params, err := checkSignature(idReq.Payload, publicKey)
    fmt.Printf("params 2: %s", params)
    return result, err
}