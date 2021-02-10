package main
 
import (
	"errors"
	"encoding/base64"
    log "github.com/log"
)

func checkSignature(payload string, key string) (map[string]interface{}, error) {

	pbkey, err := parsePublicKeyX509(key)
	if err != nil {
		log.Infof("[%s][%s][verifySignature] Error verifying signature %s", CHANNEL_ENV, JOSEUTIL, err.Error())
		return nil, errors.New(ERRORVerifying)
	}

	mesPayload, err := base64.StdEncoding.DecodeString(payload)
    if err != nil {
		log.Infof("[%s][%s][DecodeString] Decode payload %s", CHANNEL_ENV, IDREGISTRY, err)
    }

    log.Infof("[%s][%s][DecodeString] Decode payload %s", CHANNEL_ENV, IDREGISTRY, mesPayload)

	mesPayloadStr := string([]byte (mesPayload))
	
	envelope, err := NewEnvelopeFromJSON(mesPayloadStr)
    if err != nil {
		log.Infof("[%s][%s][verifySignature] Error returning envelope %s", CHANNEL_ENV, IDREGISTRY, err)
    }
	// now we validate the signature against the public key
    if err := envelope.Validate(pbkey); err != nil {
		log.Infof("[%s][%s][Validate] Envelope %s", CHANNEL_ENV, IDREGISTRY, envelope)
    }

	params := make(map[string]interface{})
	return params, nil
}