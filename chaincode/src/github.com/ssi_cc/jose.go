package main

 
import (
    "fmt"
    "strings"
    "crypto/x509"
    "encoding/json"
    "encoding/base64"
    jose "gopkg.in/square/go-jose.v2"
)

func parseKey(publicKey string) string {
    begin := "-----BEGIN PUBLIC KEY-----"
    end := "-----END PUBLIC KEY-----"

	// Replace all pairs.
    noBegin := strings.Split(publicKey, begin)
    parsed := strings.Split(noBegin[1], end)
    fmt.Printf("PublicKey: %s", parsed[0])
    return parsed[0]
}

 

func checkSignature(payload string, key string) (map[string]interface{}, error) {
    message, err := verifySignature(payload, key)

    if err != nil {
        fmt.Printf("PublicKey: %s", err)
    }

    params := make(map[string]interface{})
    err = json.Unmarshal(message, &params)

	if err != nil {
        fmt.Printf("PublicKey: %s", err)
    }
    return params, nil
}

func verifySignature(message string, key string) ([]byte, error) {

    msg, err := parseMessage(message)
    pbkey, err := parsePublicKeyX509(key)
    result, err := jose.JSONWebSignature.Verify(*msg, pbkey)

	if err != nil {
        fmt.Printf("PublicKey: %s", err)
    }

    return result, nil
}

func parseMessage(message string) (*jose.JSONWebSignature, error) {
    jwsSignature, err := jose.ParseSigned(message)

    if err != nil {
        fmt.Printf("PublicKey: %s", err)
    }
    return jwsSignature, nil
} 

func parsePublicKeyX509(publicKey string) (interface{}, error) {
    base64Data := []byte(publicKey)
    d := make([]byte, base64.StdEncoding.DecodedLen(len(base64Data)))
    n, err := base64.StdEncoding.Decode(d, base64Data)

    if err != nil {
        fmt.Printf("PublicKey: %s", err)
    }

    d = d[:n]
    publicKeyImported, err := x509.ParsePKIXPublicKey(d)

    if err != nil {
        fmt.Printf("PublicKey: %s", err)
    }
    return publicKeyImported, nil
}