package main
 
import (
	"errors"
	//"testing"
    "strings"
	"crypto/x509"
	"encoding/pem"
	"crypto/ecdsa"
	"encoding/asn1"
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

	mesPayload, err := base64.StdEncoding.DecodeString(payload)
    if err != nil {
		log.Infof("[%s][%s][DecodeString] Decode payload %s", CHANNEL_ENV, IDREGISTRY, err)
    }

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

//####################################################################################################################

func parseKey(publicKey string) string {
	begin := "-----BEGIN PUBLIC KEY-----"
	end := "-----END PUBLIC KEY-----"

	noBegin := strings.Split(publicKey, begin)
	parsed := strings.Split(noBegin[1], end)
	return parsed[0]
}

func parsePublicKeyX509(publicKey string) (*ecdsa.PublicKey, error) {
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
	log.Infof("[%s][%s][NewEnvelopeFromJSON] Envelope: %s", CHANNEL_ENV, JoseUTIL, e)
    return &e, nil
}

// Helper function to compute the SHA256 hash of the given string of bytes.
func hash(b []byte) []byte {
    h := sha256.New()
    // hash the body bytes
    h.Write(b)
    // compute the SHA256 hash
    return h.Sum(nil)
}

func (e *Envelope) Validate(publicKey *ecdsa.PublicKey) error {
    // first decode the signature to extract the DER-encoded byte string
    der	:= []byte (e.Signature)
    // unmarshal the R and S components of the ASN.1-encoded signature into our
    // signature data structure
    sig := &ECDSASignature{}
    asn1.Unmarshal(der, sig)
    // compute the SHA256 hash of our message
    h := []byte (e.Hash)
    // validate the signature!
    valid := ecdsa.Verify(
        publicKey,
        h,
        sig.R,
        sig.S,
    )
    if !valid {
        return errors.New("Signature validation failed")
    }
    // signature is valid
    return nil
}