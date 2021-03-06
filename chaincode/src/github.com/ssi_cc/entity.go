package main

import (
	"errors"
	"encoding/json"
	log "github.com/log"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) setEntity(stub shim.ChaincodeStubInterface, did string, issuer string, publicKey string) (string, error) {
	log.Infof("[%s][%s][%s][setEntity] Create Entity Identity for did %s",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, did)
	var err error
	var result string
	var issuer_ *Issuer

	issuer_, err = cc.getIssuer(stub, issuer)
	if err != nil {
		log.Errorf("[%s][%s][%s][getIDRegistry] Identity not available",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY)
		return "", err
	} else if issuer_ == nil{
		log.Errorf("[%s][%s][%s][getIDRegistry] Identity not retrieved",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY)
		return "", err
	}

	didID, err := json.Marshal(Entity{Did: did})
	if err != nil {
		log.Errorf("[%s][%s][%s][setEntity] Error parsing: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}

	identityStore, err := json.Marshal(Entity{Issuer: issuer, PublicKey: publicKey})
	if err != nil {
		log.Errorf("[%s][%s][%s][setEntity] Error parsing: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}
	
	err = stub.PutState(string(didID), identityStore)
	if err != nil {
		log.Errorf("[%s][%s][%s][setEntity] Error storing: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "", errors.New(ERRORStoringIdentity + err.Error())
	}

	log.Infof("[%s][%s][%s][setEntity] Indentity stored for Entity %s",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, did)
	result = "true"
	return result, nil
}

func (cc *Chaincode) getEntity(stub shim.ChaincodeStubInterface, did string) (string, error) {
	log.Infof("[%s][%s][%s][getEntity] Get Identity for did %s",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, did)
	idStored := Entity{}
	var err error

	didID, err := json.Marshal(Entity{Did: did})
	if err != nil {
		log.Errorf("[%s][%s][%s][getEntity] Error parsing: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}
	
	idBytes, err := stub.GetState(string(didID))
	if err != nil {
		log.Errorf("[%s][%s][%s][getEntity] Error getting identity: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "",errors.New(ERRORGetID + err.Error())
	}
	if idBytes == nil {
		log.Errorf("[%s][%s][%s][getEntity] Error the identity does not exist",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY)
		log.Errorf("[%s][%s][%s][getEntity] Return error",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY)
		return "",errors.New(ERRORnotID)
	}

	err = json.Unmarshal(idBytes, &idStored)
	if err != nil {
		log.Errorf("[%s][%s][%s][getEntity] Error parsing identity: %v",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, err.Error())
		return "", errors.New(ERRORParsingID + err.Error())
	}
	log.Infof("[%s][%s][%s][getEntity] Get PublicKey for idStored %s",uuidgen(), CHANNEL_ENV, ENTITYREGISTRY, idStored.PublicKey)

	return idStored.PublicKey, nil
}