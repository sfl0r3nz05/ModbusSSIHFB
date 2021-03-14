package main

import (
	"errors"
	"encoding/json"
	log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) setIssuer(stub shim.ChaincodeStubInterface, did string, issuer string, publicKey string) (string, error) {
	log.Infof("[%s][%s][%s][setIssuer] Create Issuer Identity for did %s",uuidgen(), CHANNEL_ENV, ISSUERREGISTRY, did)
	var result string
	var err error

	didID, err := json.Marshal(Issuer{Did: did})
	if err != nil {
		log.Errorf("[%s][%s][%s][setIssuer] Error parsing: %v",uuidgen(), CHANNEL_ENV, ISSUERREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}

	identityStore, err := json.Marshal(Issuer{Issuer: issuer, PublicKey: publicKey})
	if err != nil {
		log.Errorf("[%s][%s][%s][setIssuer] Error parsing: %v",uuidgen(), CHANNEL_ENV, ISSUERREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}
	
	err = stub.PutState(string(didID), identityStore)
	if err != nil {
		log.Errorf("[%s][%s][%s][setIssuer] Error storing: %v",uuidgen(), CHANNEL_ENV, ISSUERREGISTRY, err.Error())
		return "", errors.New(ERRORStoringIdentity + err.Error())
	}

	log.Infof("[%s][%s][%s][setIssuer] Indentity stored for issuer %s",uuidgen(), CHANNEL_ENV, ISSUERREGISTRY, did)
	result = "true"
	return result, nil
}

func (cc *Chaincode) getIssuer(stub shim.ChaincodeStubInterface, did string) (*Issuer, error) {
	log.Infof("[%s][%s][%s][getIssuer] Get Identity for did %s",uuidgen(), CHANNEL_ENV, ISSUERREGISTRY, did)
	idStored := Issuer{}
	var err error

	didID, err := json.Marshal(Issuer{Did: did})
	if err != nil {
		log.Errorf("[%s][%s][%s][getIssuer] Error parsing: %v",uuidgen(), CHANNEL_ENV, ISSUERREGISTRY, err.Error())
		return nil, errors.New(ERRORParsingID + err.Error())
	}
	
	idBytes, err := stub.GetState(string(didID))
	if err != nil {
		log.Errorf("[%s][%s][%s][getIDRegistry] Error getting identity: %v",uuidgen(), CHANNEL_ENV, IDREGISTRY, err.Error())
		return nil, errors.New(ERRORGetID + err.Error())
	}
	if idBytes == nil {
		log.Errorf("[%s][%s][%s][getIDRegistry] Error the identity does not exist",uuidgen(), CHANNEL_ENV, IDREGISTRY)
		log.Errorf("[%s][%s][%s][getIDRegistry] Return error",uuidgen(), CHANNEL_ENV, IDREGISTRY)
		return nil, errors.New(ERRORnotID)
	}

	err = json.Unmarshal(idBytes, &idStored)
	if err != nil {
		log.Errorf("[%s][%s][%s][getIssuer] Error parsing identity: %v",uuidgen(), CHANNEL_ENV, IDREGISTRY, err.Error())
		return nil, errors.New(ERRORParsingID + err.Error())
	}
	log.Infof("[%s][%s][%s][getIssuer] Get PublicKey for did %s",uuidgen(), CHANNEL_ENV, IDREGISTRY, did)

	return &idStored, nil
}