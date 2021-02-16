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
    var identity *Identity
    idReq := Request{}

    err := json.Unmarshal([]byte(args[0]), &idReq)
    log.Infof("[%s][%s][signatureVeirifed] idReq content: %v", CHANNEL_ENV, IDREGISTRY, args[0])

    identity, err = cc.getIDRegistry(stub, idReq.Did)
	if err != nil {
		log.Infof("[%s][%s][verifyArgs] Identity not available", CHANNEL_ENV, IDREGISTRY)
        log.Infof("[%s][%s][verifyArgs] Creating an identity ...", CHANNEL_ENV, IDREGISTRY)

        identityStore := Identity{PublicKey: idReq.PublicKey}
        _, err = cc.createIDRegistry(stub, idReq.Did, identityStore)
        if err != nil {
            log.Errorf("[%s][%s][verifyArgs][CreateIdentity] Error parsing: %v", CHANNEL_ENV, err.Error())
            return "", err
        }
        log.Infof("[%s][%s][verifyArgs] created identity", CHANNEL_ENV, IDREGISTRY)
	}

    //log.Infof("[%s][%s][pubKeyRecovered] Ready To Verify Signature", CHANNEL_ENV, IDREGISTRY)
	//params, err := checkSignature(idReq.Payload, identity.PublicKey)

    //log.Infof("[%s][%s][signatureVeirifed] Ready To Read Payload", CHANNEL_ENV, IDREGISTRY)

    fmt.Printf("params 2: %s", params)
    
    return result, err
}