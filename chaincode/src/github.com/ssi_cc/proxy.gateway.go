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
		log.Errorf("[%s][%s][checkArgs] Error recovering identity: %v", CHANNEL_ENV, IDREGISTRY, err.Error())
		return "", err
	}

    log.Infof("[%s][%s][didRecovered] Ready To Verify Public Key", CHANNEL_ENV, IDREGISTRY)
	publicKey = parseKey(identity.PublicKey)

    log.Infof("[%s][%s][pubKeyRecovered] Ready To Verify Signature", CHANNEL_ENV, IDREGISTRY)
	params, err := checkSignature(idReq.Payload, identity.PublicKey)

    log.Infof("[%s][%s][signatureVeirifed] Ready To Read Payload", CHANNEL_ENV, IDREGISTRY)

    fmt.Printf("params 2: %s", params)
    
    return result, err
}