package main
 
import (
	"errors"
	//"testing"
    "strings"
	"crypto/x509"
	"encoding/pem"
	"crypto/ecdsa"
	//"encoding/asn1"
	"encoding/json"
	"crypto/sha256"
	"encoding/base64"
    log "github.com/log"
)

func checkSignature(payload string, key string) (map[string]interface{}, error) {

	pbkey, err := parsePublicKeyX509(key)
	if err != nil {
		log.Infof("[%s][%s][verifySignature] Error verifying signature %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORVerifying)
	}

	log.Infof("[%s][%s][verifySignature] Get key pbkey %s", CHANNEL_ENV, IDREGISTRY, pbkey)

	parsedArray, err := parsePayload(payload)
	if err != nil {
		log.Infof("[%s][%s][verifySignature] Failed to parse ECDSA public key %s", CHANNEL_ENV, JoseUTIL, err.Error())
		return nil, errors.New(ERRORVerifying)
	}

	mesPayloadBase64 := parsedArray[0]
	signature := parsedArray[1]

	log.Infof("[%s][%s][verifySignature] Get key hash %s", CHANNEL_ENV, IDREGISTRY, hash)
	log.Infof("[%s][%s][verifySignature] Get key signature %s", CHANNEL_ENV, IDREGISTRY, signature)

	mesPayload, err := base64.StdEncoding.DecodeString(mesPayloadBase64)
    if err != nil {
		log.Infof("[%s][%s][verifySignature] Get key signature %s", CHANNEL_ENV, IDREGISTRY, err)
    }

	log.Infof("[%s][%s][verifySignature] Message %s", CHANNEL_ENV, IDREGISTRY, mesPayload)

	mesPayloadStr := string([]byte (mesPayload))

	log.Infof("[%s][%s][verifySignature] Message Byte %s", CHANNEL_ENV, IDREGISTRY, mesPayloadStr)

	log.Infof("[%s][%s][verifySignature] Message Byte %s", CHANNEL_ENV, IDREGISTRY, TestMessage)
	
	envelope, err := NewEnvelopeFromJSON(mesPayloadStr)
    if err != nil {
		log.Infof("[%s][%s][verifySignature] Error %s", CHANNEL_ENV, IDREGISTRY, err)
    }

	log.Infof("[%s][%s][verifySignature] Get key signature %s", CHANNEL_ENV, IDREGISTRY, envelope)

	params := make(map[string]interface{})
	return params, nil
}

//####################################################################################################################

func parseKey(publicKey string) string {
	begin := "-----BEGIN PUBLIC KEY-----"
	end := "-----END PUBLIC KEY-----"

	noBegin := strings.Split(publicKey, begin)
	parsed := strings.Split(noBegin[1], end)
	return parsed[0]
}

func parsePublicKeyX509(publicKey string) (interface{}, error) {
	block, _ := pem.Decode([]byte(publicKey))
	if block == nil {
		return nil, errors.New("Failed to decode PEM public key") // ERROR MUST BE COMPLIANT
	}

	log.Infof("[%s][%s][parsePublicKeyX509] block %s", CHANNEL_ENV, JoseUTIL, block)

	pub, err := x509.ParsePKIXPublicKey(block.Bytes)
    if err != nil {
        return nil, errors.New("Failed to parse ECDSA public key")	// ERROR MUST BE COMPLIANT
    }
    switch pub := pub.(type) {
    case *ecdsa.PublicKey:
        return pub, nil
    }
    return nil, errors.New("Unsupported public key type")
}

// Attempts to create a new envelope structure from the given JSON string.
func NewEnvelopeFromJSON(s string) (*Envelope, error) {
    var e Envelope

    if err := json.Unmarshal([]byte(s), &e); err != nil {
        return nil, err
    }
	
    // now attempt to unmarshal the message body itself from the raw message
    var body Controller
    if err := json.Unmarshal(e.RawMessage, &body); err != nil {
        return nil, err
    }
    e.Message = body
	log.Infof("[%s][%s][parsePublicKeyX509] body %s", CHANNEL_ENV, JoseUTIL, body)
    return &e, nil
}

func parsePayload(payload string) ([]string, error) {
	dot := "."

	parsed := strings.Split(payload, dot)
	if parsed == nil {
		return nil, errors.New("Failed split payload") // ERROR MUST BE COMPLIANT
	}
	return parsed, nil
}

// Helper function to compute the SHA256 hash of the given string of bytes.
func hash(b []byte) []byte {
    h := sha256.New()
    // hash the body bytes
    h.Write(b)
    // compute the SHA256 hash
    return h.Sum(nil)
}