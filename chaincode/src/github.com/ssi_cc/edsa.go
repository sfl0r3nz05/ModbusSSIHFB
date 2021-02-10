package main
 
import (
	"errors"
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

	log.Infof("[%s][%s][parsePublicKeyX509] block %s", CHANNEL_ENV, JOSEUTIL, block)

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
    
    // unmarshal the R and S components of the ASN.1-encoded signature into our
    signature, err := base64.StdEncoding.DecodeString(e.Signature)
    if err != nil {
        log.Errorf("[%s][%s][Validate] Signature decoding failure", CHANNEL_ENV, JOSEUTIL)
        return err
    }

    // unmarshal the R and S components of the ASN.1-encoded signature into our
    has, err := base64.StdEncoding.DecodeString(e.Hash)
    if err != nil {
        log.Errorf("[%s][%s][Validate] Hash decoding failure", CHANNEL_ENV, JOSEUTIL)
        return err
    }
    
    // signature data structure
    sig := &ECDSASignature{}
    _, err = asn1.Unmarshal(signature, sig)
    if err != nil {
        log.Errorf("[%s][%s][ECDSASignature] ECDSASignature failure", CHANNEL_ENV, JOSEUTIL)
        return err
    }

    // validate the signature!
    valid := ecdsa.Verify(
        publicKey,
        has,
        sig.R,
        sig.S,
    )
    if !valid {
        log.Errorf("[%s][%s][Verify] Verify failure", CHANNEL_ENV, JOSEUTIL)
        return errors.New("Signature validation failed")
    }
    // signature is valid
    return nil
}

//####################################################################################################################