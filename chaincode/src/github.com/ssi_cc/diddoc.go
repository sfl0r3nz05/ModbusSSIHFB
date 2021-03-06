package main

import (
	"errors"
	"encoding/json"
	log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) setDidDoc(stub shim.ChaincodeStubInterface, did string, context string, signature string, countersignature string, auth_id string, auth_type string, auth_issuer string, auth_Public string, serv_id string, serv_type string, serv_endpoint string, serv_func string, serv_start string, serv_offset string, serv_generator string, serv_plainNumber string) (string, error) {
	log.Infof("[%s][%s][%s][setDidDoc] Create DidDoc for did %s",uuidgen(), CHANNEL_ENV, DIDDOCREGISTRY, did)
	var result string
	var err error

	log.Infof("[%s][%s][%s][setDidDoc] Create context for did %s",uuidgen(), CHANNEL_ENV, DIDDOCREGISTRY, context)

	didID, err := json.Marshal(DidDoc{Did: did})
	if err != nil {
		log.Errorf("[%s][%s][%s][setDidDoc] Error parsing: %v",uuidgen(), CHANNEL_ENV, DIDDOCREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}

	diDocStore, err := json.Marshal(DidDoc{Context: context, Signature: signature, Countersignature: countersignature, AuthId: auth_id, AuthType: auth_type, AuthIssuer: auth_issuer, AuthPublicKeyBase58: auth_Public, ServiceId: serv_id, ServiceType: serv_type, ServiceEndPoint: serv_endpoint, ServiceFunctCode: serv_func, ServiceStartAddr: serv_start, ServiceOffset: serv_offset, ServiceGenerator: serv_generator, ServicePlainNumber: serv_plainNumber})
	if err != nil {
		log.Errorf("[%s][%s][%s][setDidDoc] Error parsing: %v",uuidgen(), CHANNEL_ENV, DIDDOCREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}
	
	err = stub.PutState(string(didID), diDocStore)
	if err != nil {
		log.Errorf("[%s][%s][%s][setDidDoc] Error storing: %v",uuidgen(), CHANNEL_ENV, DIDDOCREGISTRY, err.Error())
		return "", errors.New(ERRORStoringIdentity + err.Error())
	}

	log.Infof("[%s][%s][%s][setDidDoc] DidDoc stored for entity %s",uuidgen(), CHANNEL_ENV, DIDDOCREGISTRY, did)
	result = "true"
	return result, nil
}


func (cc *Chaincode) getDidDoc(stub shim.ChaincodeStubInterface, did string) (string, error) {
	log.Infof("[%s][%s][%s][getDidDoc] Get Identity for did %s",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, did)
	idStored := DidDoc{}
	var err error

	didID, err := json.Marshal(DidDoc{Did: did})
	if err != nil {
		log.Errorf("[%s][%s][%s][getDidDoc] Error parsing: %v",uuidgen(), CHANNEL_ENV, DIDDOCREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}	
	idBytes, err := stub.GetState(string(didID))
	if err != nil {
		log.Errorf("[%s][%s][%s][getDidDoc] Error getting identity: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "",errors.New(ERRORGetID + err.Error())
	}
	if idBytes == nil {
		log.Errorf("[%s][%s][%s][getDidDoc] Error the identity does not exist",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY)
		log.Errorf("[%s][%s][%s][getDidDoc] Return error",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY)
		return "",errors.New(ERRORnotID)
	}
	err = json.Unmarshal(idBytes, &idStored)
	if err != nil {
		log.Errorf("[%s][%s][%s][getDidDoc] Error parsing identity: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}
	log.Infof("[%s][%s][%s][getDidDoc] Get PublicKey for idStored %s",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, idStored)

	out, err := json.Marshal(idStored)
    if err != nil {
        panic (err)
    }

	return string(out), nil
}