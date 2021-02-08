package main
 
import (
	"errors"
    "strings"
	"crypto/x509"
	"encoding/pem"
	"encoding/json"
    log "github.com/log"
    jose "gopkg.in/square/go-jose.v2"
)

func checkSignature(payload string, key string) (map[string]interface{}, error) {
	object, err := parseMessage(payload)
	
	pbkey, err := parsePublicKeyX509(key)
	log.Infof("[%s][%s][verifySignature] Get key parsed %s", CHANNEL_ENV, IDREGISTRY, pbkey)
	
	message, err := jose.JSONWebSignature.Verify(*object, pbkey)

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
	begin := "-----BEGIN CERTIFICATE-----"
	end := "-----END CERTIFICATE-----"

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
	log.Infof("[%s][%s][parseMessage] publicKey %s", CHANNEL_ENV, JoseUTIL, publicKey)

	block, _ := pem.Decode([]byte(publicKey))
	log.Infof("[%s][%s][parseMessage] publicKey2 %s", CHANNEL_ENV, JoseUTIL, block)

	if block == nil {
		panic("failed to parse PEM block containing the public key")
	}

	publicKeyImported, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		log.Infof("[%s][%s][parsePublicKeyX509] Error parsing into X509 %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORParseX509)
	}

	log.Infof("[%s][%s][parseMessage] Conocer el valor de publicKeyImported %s", CHANNEL_ENV, JoseUTIL, publicKeyImported)

	return publicKeyImported, nil
}