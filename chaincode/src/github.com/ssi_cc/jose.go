package main
 
import (
	"errors"
    "strings"
	"crypto/x509"
	"encoding/pem"
	//"crypto/ecdsa"
	"encoding/json"
	//"encoding/base64"
    log "github.com/log"
    jose "gopkg.in/square/go-jose.v2"
)

func checkSignature(payload string, key string) (map[string]interface{}, error) {
	msg, err := parseMessage(payload)
	log.Infof("[%s][%s][verifySignature] Get message parsed %s", CHANNEL_ENV, IDREGISTRY, msg)

	pbkey, err := parsePublicKeyX509(key)
	log.Infof("[%s][%s][verifySignature] Get key parsed %s", CHANNEL_ENV, IDREGISTRY, pbkey)
	
	message, err := jose.JSONWebSignature.Verify(*msg, pbkey)

	if err != nil {
		log.Infof("[%s][%s][verifySignature] Error verifying signature %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORVerifying)
	}

	params := make(map[string]interface{})

	err = json.Unmarshal(message, &params)
	if err != nil {
		log.Errorf("[%s][%s][checkSignature] Error parsing: %v", CHANNEL_ENV, IDGATEWAY, err.Error())
		return nil, errors.New(ERRORParsingData)
	}
	return params, nil
}

func parseKey(publicKey string) string {
	begin := "-----BEGIN PUBLIC KEY-----"
	end := "-----END PUBLIC KEY-----"

	noBegin := strings.Split(publicKey, begin)
	parsed := strings.Split(noBegin[1], end)
	return parsed[0]
}

func parseMessage(message string) (*jose.JSONWebSignature, error) {
	jwsSignature, err := jose.ParseSigned(message)
	if err != nil {
		log.Infof("[%s][%s][parseMessage] Error parsing into JWS %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORParseJWS)
	}
	return jwsSignature, nil
}

func parsePublicKeyX509(publicKey string) (interface{}, error) {
	block, _ := pem.Decode([]byte(publicKey))
	if block == nil {
		panic("failed to parse PEM block containing the public key")
	}

	log.Infof("[%s][%s][parsePublicKeyX509] block %s", CHANNEL_ENV, JoseUTIL, block)

	publicKeyImported, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		panic("failed to parse DER encoded public key: " + err.Error())
	}
	return publicKeyImported, nil
}