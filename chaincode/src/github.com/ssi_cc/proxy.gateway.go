package main

import (
	"encoding/json"
    log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) verifyArgs(stub shim.ChaincodeStubInterface, args []string) (string, error) {
    log.Infof("[%s][%s][%s][verifyArgs] Get Identity",uuidgen(), CHANNEL_ENV, IDGATEWAY)
    var diddoc DidDoc
    var result string
    var issuer Issuer
    var entity Entity
    idReq := Request{}
    var identity *Identity

    err := json.Unmarshal([]byte(args[0]), &idReq)
    log.Infof("[%s][%s][%s][verifyArgs] idReq content: %v",uuidgen(), CHANNEL_ENV, IDREGISTRY, args[0])

    identity, err = cc.getIDRegistry(stub, idReq.Did)
	if err != nil {
		log.Infof("[%s][%s][%s][verifyArgs][getIDRegistry] Identity not available",uuidgen(), CHANNEL_ENV, IDREGISTRY)
        log.Infof("[%s][%s][%s][verifyArgs][getIDRegistry] Creating an identity ...",uuidgen(), CHANNEL_ENV, IDREGISTRY)

        identityStore := Identity{PublicKey: idReq.PublicKey}
        _, err = cc.createIDRegistry(stub, idReq.Did, identityStore)
        if err != nil {
            log.Errorf("[%s][%s][%s][verifyArgs][CreateIdentity] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }
        log.Infof("[%s][%s][%s][verifyArgs][CreateIdentity] Created identity",uuidgen(), CHANNEL_ENV, IDREGISTRY)
        
        result = "true"
        return result, err
	}

	method, params, err := checkSignature(idReq.Payload, identity.PublicKey)
    
    if method == "setIssuer" {
		log.Infof("[%s][%s][verifyArgs][setIssuer] Params: %s",uuidgen(), CHANNEL_ENV, params)
        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][%s][setIssuer] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }

        err = json.Unmarshal([]byte(jsonStr), &issuer)
        if err != nil {
            log.Errorf("[%s][%s][%s][setIssuer] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }
        result, err = cc.setIssuer(stub, issuer.Did, issuer.Issuer, issuer.PublicKey)
	}
    if method == "getIssuer" {
		log.Infof("[%s][%s][verifyArgs][getIssuer] Params: %s",uuidgen(), CHANNEL_ENV, params)
	}
    if method == "setEntity" {
		log.Infof("[%s][%s][verifyArgs][setEntity] Params: %s",uuidgen(), CHANNEL_ENV, params)
        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][%s][setEntity] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }

        err = json.Unmarshal([]byte(jsonStr), &entity)
        if err != nil {
            log.Errorf("[%s][%s][%s][setEntity] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }
        result, err = cc.setEntity(stub, entity.Did, entity.Issuer, entity.PublicKey)
	}
    if method == "getEntity" {
		log.Infof("[%s][%s][verifyArgs][getEntity] Params: %s",uuidgen(), CHANNEL_ENV, params)
        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][%s][getEntity] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }

        err = json.Unmarshal([]byte(jsonStr), &entity)
        if err != nil {
            log.Errorf("[%s][%s][%s][getEntity] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }
        log.Infof("[%s][%s][verifyArgs][CreateIdentity] Params: %s",uuidgen(), CHANNEL_ENV, entity)
        result, err = cc.getEntity(stub, entity.Did)
        log.Infof("[%s][%s][getEntity] Params: %s",uuidgen(), CHANNEL_ENV, result)
	}
    if method == "setDidDoc" {
		log.Infof("[%s][%s][verifyArgs][setDidDoc] Params: %s",uuidgen(), CHANNEL_ENV, params)

        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][%s][verifyArgs][setDidDoc] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }

        err = json.Unmarshal([]byte(jsonStr), &diddoc)
        if err != nil {
            log.Errorf("[%s][%s][%s][verifyArgs][setDidDoc] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }
        log.Infof("[%s][%s][verifyArgs][setDidDoc] diddoc: %s",uuidgen(), CHANNEL_ENV, diddoc)
        result, err = cc.setDidDoc(stub, diddoc.Did, diddoc.Context, diddoc.Signature, diddoc.Countersignature, diddoc.Authentication[0].Id, diddoc.Authentication[0].Type, diddoc.Authentication[0].Issuer, diddoc.Authentication[0].PublicKeyBase58,  diddoc.Service[0].Id, diddoc.Service[0].Type, diddoc.Service[0].ServiceEndpoint, diddoc.Service[0].FunctionCode, diddoc.Service[0].StartingAddress, diddoc.Service[0].Offset, diddoc.Service[0].Generator, diddoc.Service[0].PlainNumber)
	}
    if method == "getDidDoc" {
		log.Infof("[%s][%s][verifyArgs][getDidDoc] Params: %s",uuidgen(), CHANNEL_ENV, params)
        jsonStr, err := json.Marshal(params)
        if err != nil {
            log.Errorf("[%s][%s][%s][getDidDoc] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }
        err = json.Unmarshal([]byte(jsonStr), &diddoc)
        if err != nil {
            log.Errorf("[%s][%s][%s][getDidDoc] Error parsing: %v",uuidgen(), CHANNEL_ENV, err.Error())
            return "", err
        }
        log.Infof("[%s][%s][verifyArgs][getDidDoc] Params: %s",uuidgen(), CHANNEL_ENV, entity)
        result, err = cc.getDidDoc(stub, diddoc.Did)
        log.Infof("[%s][%s][getDidDoc] Params: %s",uuidgen(), CHANNEL_ENV, result)
	}
    
    return result, err
}