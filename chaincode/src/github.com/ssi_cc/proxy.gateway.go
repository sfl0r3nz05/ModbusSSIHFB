package main

import (
	"fmt"
	"encoding/json"
	"github.com/hyperledger/fabric/core/chaincode/shim"
)

func (cc *Chaincode) verifyArgs(stub shim.ChaincodeStubInterface, args []string) (string, error) {
    var result string
    idReq := Request{}
    var publicKey string
    var identity *Identity
    err := json.Unmarshal([]byte(args[0]), &idReq)


    if idReq.PublicKey != "" {
        publicKey = parseKey(idReq.PublicKey)
        fmt.Printf("PublicKey: %s", publicKey)
        params, err := checkSignature(idReq.Payload, publicKey)
        fmt.Printf("PublicKey: %s", params)
        fmt.Printf("PublicKey: %s", err)
    }

    identity, err = cc.getIDRegistry(stub, idReq.Did)

    if err != nil {
        return "", err
    }

    publicKey = parseKey(identity.PublicKey)
    params, err := checkSignature(idReq.Payload, publicKey)
    fmt.Printf("PublicKey: %s", params)
    return result, err
}