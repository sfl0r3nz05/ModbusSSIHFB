package main

import (
	"encoding/json"
    log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) verifyArgs(stub shim.ChaincodeStubInterface, args []string) (string, error) {
    log.Infof("[%s][%s][checkArgs] Get Identity", CHANNEL_ENV, IDGATEWAY)
    var diddoc DidDoc
    var result string
    var issuer Issuer
    var entity Entity
    idReq := Request{}
    var identity *Identity

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
        
        result = "true"
        return result, err
	}

	method, params, err := checkSignature(idReq.Payload, identity.PublicKey)
    
    if method == "setIssuer" {
		log.Infof("[%s][verifyArgs][CreateIdentity] Params: %s", CHANNEL_ENV, params)
        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][verifyArgs] Error parsing: %v", CHANNEL_ENV, err.Error())
            return "", err
        }

        err = json.Unmarshal([]byte(jsonStr), &issuer)
        if err != nil {
            log.Errorf("[%s][%s][verifyArgs] Error parsing: %v", CHANNEL_ENV, err.Error())
            return "", err
        }
        result, err = cc.setIssuer(stub, issuer.Did, issuer.Issuer, issuer.PublicKey)
	}
    if method == "getIssuer" {
		log.Infof("[%s][verifyArgs][CreateIdentity] Params: %s", CHANNEL_ENV, params)
	}
    if method == "setEntity" {
		log.Infof("[%s][verifyArgs][CreateIdentity] Params: %s", CHANNEL_ENV, params)
        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][verifyArgs] Error parsing: %v", CHANNEL_ENV, err.Error())
            return "", err
        }

        err = json.Unmarshal([]byte(jsonStr), &entity)
        if err != nil {
            log.Errorf("[%s][%s][verifyArgs] Error parsing: %v", CHANNEL_ENV, err.Error())
            return "", err
        }
        result, err = cc.setEntity(stub, entity.Did, entity.Issuer, entity.PublicKey)
	}
    if method == "getEntity" {
		log.Infof("[%s][verifyArgs][CreateIdentity] Params: %s", CHANNEL_ENV, params)
	}
    if method == "setDidDoc" {
		log.Infof("[%s][verifyArgs][CreateIdentity] Params: %s", CHANNEL_ENV, params)

        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][verifyArgs] Error parsing: %v", CHANNEL_ENV, err.Error())
            return "", err
        }

        err = json.Unmarshal([]byte(jsonStr), &diddoc)
        if err != nil {
            log.Errorf("[%s][%s][verifyArgs] Error parsing: %v", CHANNEL_ENV, err.Error())
            return "", err
        }
        log.Infof("[%s][verifyArgs][CreateIdentity] diddoc: %s", CHANNEL_ENV, diddoc)
        log.Infof("[%s][verifyArgs][CreateIdentity] Authentication: %s", CHANNEL_ENV, diddoc.Authentication[0].Id)
        log.Infof("[%s][verifyArgs][CreateIdentity] Service: %s", CHANNEL_ENV, diddoc.Service[0].ServiceEndpoint)

        result, err = cc.setDidDoc(stub, diddoc.Did, diddoc.Context, diddoc.Signature, diddoc.Countersignature, diddoc.Authentication[0].Id, diddoc.Authentication[0].Issuer, diddoc.Authentication[0].PublicKeyBase58, diddoc.Authentication[0].Type, diddoc.Service[0].ServiceEndpoint, diddoc.Service[0].FunctionCode, diddoc.Service[0].Id,diddoc.Service[0].Offset, diddoc.Service[0].StartingAddress, diddoc.Service[0].Type)
	}
    if method == "getDidDoc" {
		log.Infof("[%s][verifyArgs][CreateIdentity] Params: %s", CHANNEL_ENV, params)
	}
    
    return result, err
}