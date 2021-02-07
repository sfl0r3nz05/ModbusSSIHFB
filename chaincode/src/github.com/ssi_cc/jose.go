package main

 
import (
	"errors"
    "strings"
    "crypto/x509"
    "encoding/json"
    "encoding/base64"
    log "github.com/log"
    jose "gopkg.in/square/go-jose.v2"
)

func parseKey(publicKey string) string {

	begin := "-----BEGIN PUBLIC KEY-----"
	end := "-----END PUBLIC KEY-----"

	noBegin := strings.Split(publicKey, begin)
	parsed := strings.Split(noBegin[1], end)
	return parsed[0]
}

func checkSignature(payload string, key string) (map[string]interface{}, error) {
	log.Errorf("[%s][%s][checkSignature] Verifying signature", CHANNEL_ENV, IDGATEWAY)

	message, err := verifySignature(payload, key)
	if err != nil {
		log.Errorf("[%s][%s][checkSignature] Error verifying signature: %v", CHANNEL_ENV, IDGATEWAY, err.Error())
		return nil, errors.New(ERRORVerSign)
	}
	params := make(map[string]interface{})

	err = json.Unmarshal(message, &params)
	if err != nil {
		log.Errorf("[%s][%s][checkSignature] Error parsing: %v", CHANNEL_ENV, IDGATEWAY, err.Error())
		return nil, errors.New(ERRORParsingData)
	}
	return params, nil
}

func verifySignature(message string, key string) ([]byte, error) {
	msg, err := parseMessage(message)
	pbkey, err := parsePublicKeyX509(key)
	result, err := jose.JSONWebSignature.Verify(*msg, pbkey)
	if err != nil {
		log.Infof("[%s][%s][verifySignature] Error verifying signature %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORVerifying)
	}
	return result, nil
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
	base64Data := []byte(publicKey)

	d := make([]byte, base64.StdEncoding.DecodedLen(len(base64Data)))
	n, err := base64.StdEncoding.Decode(d, base64Data)
	if err != nil {
		log.Infof("[%s][%s][parsePublicKeyX509] Error decoding into base64 %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORBase64)
	}
	d = d[:n]

	publicKeyImported, err := x509.ParsePKIXPublicKey(d)
	if err != nil {
		log.Infof("[%s][%s][parsePublicKeyX509] Error parsing into X509 %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORParseX509)
	}
	return publicKeyImported, nil
}