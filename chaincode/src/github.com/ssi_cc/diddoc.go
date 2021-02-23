package main

import (
	"errors"
	"encoding/json"
	log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) setDidDoc(stub shim.ChaincodeStubInterface, did string, context string, signature string, countersignature string, auth_id string, auth_issuer string, auth_Public string, auth_Type string, serv_serv string, serv_func string, serv_id string, serv_offset string, serv_start string, serv_type string) (string, error) {
	log.Infof("[%s][%s][setDidDoc] Create DidDoc for did %s", CHANNEL_ENV, DIDDOCREGISTRY, did)
	var result string
	var err error

	log.Infof("[%s][%s][setDidDoc] Create context for did %s", CHANNEL_ENV, DIDDOCREGISTRY, context)

	didID, err := json.Marshal(DidDoc{Did: did})
	if err != nil {
		log.Errorf("[%s][%s][setDidDoc] Error parsing: %v", CHANNEL_ENV, DIDDOCREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}

	diDocStore, err := json.Marshal(DidDoc{Context: context, Signature: signature, Countersignature: countersignature})
	if err != nil {
		log.Errorf("[%s][%s][setDidDoc] Error parsing: %v", CHANNEL_ENV, DIDDOCREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}
	
	err = stub.PutState(string(didID), diDocStore)
	if err != nil {
		log.Errorf("[%s][%s][setDidDoc] Error storing: %v", CHANNEL_ENV, DIDDOCREGISTRY, err.Error())
		return "", errors.New(ERRORStoringIdentity + err.Error())
	}

	log.Infof("[%s][%s][setDidDoc] DidDoc stored for entity %s", CHANNEL_ENV, DIDDOCREGISTRY, did)
	result = "true"
	return result, nil
}