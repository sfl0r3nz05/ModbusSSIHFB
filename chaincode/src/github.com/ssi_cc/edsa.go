package main
 
import (
	"errors"
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

func parsePublicKeyX509(publicKey string) (*ecdsa.PublicKey, error) {
	block, _ := pem.Decode([]byte(publicKey))
	if block == nil {
		return nil, errors.New("Failed to decode PEM public key") // ERROR MUST BE COMPLIANT
	}
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

func (e *Envelope) Validate(publicKey *ecdsa.PublicKey) (string, interface{}, error) {
    // unmarshal the R and S components of the ASN.1-encoded signature into our
    signature, err := base64.StdEncoding.DecodeString(e.Signature)
    if err != nil {
        log.Errorf("[%s][%s][Validate] Signature decoding failure", CHANNEL_ENV, JOSEUTIL)
        return "", "", err
    }

    // unmarshal the R and S components of the ASN.1-encoded signature into our
    has, err := base64.StdEncoding.DecodeString(e.Hash)
    if err != nil {
        log.Errorf("[%s][%s][Validate] Hash decoding failure", CHANNEL_ENV, JOSEUTIL)
        return "", "", err
    }

    // signature data structure
    sig := &ECDSASignature{}
    _, err = asn1.Unmarshal(signature, sig)
    if err != nil {
        log.Errorf("[%s][%s][ECDSASignature] ECDSASignature failure", CHANNEL_ENV, JOSEUTIL)
        return "", "", err
    }

    // validate the signature!
    valid := ecdsa.Verify(
        publicKey,
        has,
        sig.R,
        sig.S,
    )
    // signature is valid
    if !valid {
        log.Errorf("[%s][%s][Verify] Signature verification failure", CHANNEL_ENV, JOSEUTIL)
        return "", "", errors.New("Signature validation failed")
    }
    return e.Method, e.Params, nil
}
//####################################################################################################################