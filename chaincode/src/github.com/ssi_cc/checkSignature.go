package main
 
import (
	"errors"
	"encoding/base64"
    log "github.com/log"
)

func checkSignature(payload string, key string) (string, interface{}, error) {

	pbkey, err := parsePublicKeyX509(key)
	if err != nil {
		log.Infof("[%s][%s][checkSignature] Error verifying signature %s", CHANNEL_ENV, JOSEUTIL, err.Error())
		return "", nil, errors.New(ERRORVerifying)
	}

	mesPayload, err := base64.StdEncoding.DecodeString(payload)
    if err != nil {
		log.Infof("[%s][%s][checkSignature] Decode payload %s", CHANNEL_ENV, IDREGISTRY, err)
    }

	mesPayloadStr := string([]byte (mesPayload))
	
	envelope, err := NewEnvelopeFromJSON(mesPayloadStr)
    if err != nil {
		log.Infof("[%s][%s][checkSignature] Error returning envelope %s", CHANNEL_ENV, IDREGISTRY, err)
    }

    method, result, err := envelope.Validate(pbkey); 
	if err != nil {
		log.Infof("[%s][%s][Validate] Envelope %s", CHANNEL_ENV, IDREGISTRY, envelope)
    }
	return method, result, nil
}