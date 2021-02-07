package main

import (
	"errors"
	"encoding/json"
	log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

var ccErrorCode = "CC-01"

func (cc *Chaincode) createIDRegistry(stub shim.ChaincodeStubInterface, did string, identity Identity) (string, error) {
	log.Infof("[%s][%s][createIDRegistry] Create Identity for did %s", CHANNEL_ENV, IDREGISTRY, did)
	bytes, err := stub.GetState(did)

	if bytes != nil {
		log.Errorf("[%s][%s][createIDRegistry] The identity already exists", CHANNEL_ENV, IDREGISTRY)
		log.Errorf("[%s][%s][createIDRegistry] Return error", CHANNEL_ENV, IDREGISTRY)
		return "", errors.New(ERRORIDExists)
	}

	idBytes, err := json.Marshal(identity)
	if err != nil {
		log.Errorf("[%s][%s][createIDRegistry] Error parsing: %v", CHANNEL_ENV, IDREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}

	err = stub.PutState(did, idBytes)
	if err != nil {
		log.Errorf("[%s][%s][createIDRegistry] Error storing: %v", CHANNEL_ENV, IDREGISTRY, err.Error())
		return "", errors.New(ERRORStoringIdentity + err.Error())
	}
	log.Infof("[%s][%s][createIDRegistry] Indentity stored for did %s", CHANNEL_ENV, IDREGISTRY, did)

	return "", nil
}

func (cc *Chaincode) getIDRegistry(stub shim.ChaincodeStubInterface, did string) (*Identity, error) {

	log.Infof("[%s][%s][getIDRegistry] Get Identity for did %s", CHANNEL_ENV, IDREGISTRY, did)
	idStored := Identity{}
	idBytes, err := stub.GetState(did)
	if err != nil {
		log.Errorf("[%s][%s][getIDRegistry] Error getting identity: %v", CHANNEL_ENV, IDREGISTRY, err.Error())
		return nil, errors.New(ERRORGetID + err.Error())
	}
	if idBytes == nil {
		log.Errorf("[%s][%s][getIDRegistry] Error the identity does not exist", CHANNEL_ENV, IDREGISTRY)
		log.Errorf("[%s][%s][getIDRegistry] Return error", CHANNEL_ENV, IDREGISTRY)
		return nil, errors.New(ERRORnotID)
	}
	err = json.Unmarshal(idBytes, &idStored)
	if err != nil {
		log.Errorf("[%s][%s][getIDRegistry] Error parsing identity: %v", CHANNEL_ENV, IDREGISTRY, err.Error())
		return nil, errors.New(ERRORParsingID + err.Error())
	}
	log.Infof("[%s][%s][getIDRegistry] Get PublicKey for did %s", CHANNEL_ENV, IDREGISTRY, did)

	return &idStored, nil
}