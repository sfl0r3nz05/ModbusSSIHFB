package main

import (
	"math/big"
)

// Identity stored in bc
type Identity struct {
	Did 	   string `json:"did,omitempty"`
	PublicKey  string `json:"publicKey"`
}

// Entity's identity stored in bc
type Entity struct {
	Did       string `json:"did,omitempty"`
	Issuer string `json:"issuer,omitempty"`
	PublicKey string `json:"publicKey,omitempty"`
}

// Issuer's identity stored in bc
type Issuer struct {
	Did       string `json:"did,omitempty"`
	Issuer string `json:"issuer,omitempty"`
	PublicKey string `json:"publicKey,omitempty"`
}

// IdentityRequest to serialize args
type DidDoc struct {
	Did        string `json:"did"`
	Controller string `json:"controller,omitempty"`
	PublicKey  string `json:"publicKey"`
	Payload    string `json:"payload,omitempty"` // me pasa una firma // el controller lo meto yo
	Access     int    `json:"access,omitempty"`
}

type IdentityRequest struct {
	Did        string `json:"did"`
	Controller string `json:"controller,omitempty"`
	PublicKey  string `json:"publicKey"`
	Payload    string `json:"payload,omitempty"` // me pasa una firma // el controller lo meto yo
}

// Request to serialize args
type Request struct {
	Did       string `json:"did,omitempty"`
	PublicKey string `json:"publicKey,omitempty"`
	Payload   string `json:"payload,omitempty"` // me pasa una firma // el controller lo meto yo
}

// Encapsulates the overall message we're trying to decode and validate.
type Envelope struct {
    //Did	string	`json:"did"`
	Method	string	`json:"method"`
	Params	map[string]interface{} `json:"params,omitempty"`
    PublicKey	string	`json:"publicKey"`
	Hash	string	`json:"hash"`
	Signature	string	`json:"signature"`
}

type ECDSASignature struct {
    R, S *big.Int
}

// Error responses
const (
	ERRORWrongNumberArgs  = `Wrong number of arguments. Expecting a JSON with token information.`
	ERRORParsingData      = `Error parsing data `
	ERRORPutState         = `Failed to store data in the ledger.	`
	ERRORGetState         = `Failed to get data from the ledger. `
	ERRORDelState         = `Failed to delete data from the ledger. `
	ERRORChaincodeCall    = `Error calling chaincode`
	ERRORGetService       = `Error getting service`
	ERRORUpdService       = `Error updating service`
	ERRORServiceNotExists = `Error The service doesn't exist`
	ErrNotECPublicKey  	  = `Key is not a valid ECDSA public key`
	ErrNotECPrivateKey 	  = `Key is not a valid ECDSA private key`
	ErrKeyMustBePEMEncoded = `Key is not a valid PEM format`
	ERRORCreatingService  = `Error storing service`
	ERRORParsingService   = `Error parsing service`
	ERRORServiceExists    = `The service already exists in registry`
	ERRORDidMissing       = `Error calling service, no service DID Specified`
	ERRORStoringIdentity  = `Error storing identity`
	ERRORUpdatingID       = `Error updating identity in ledger`
	ERRORGetID            = `Error getting identity`
	ERRORVerID            = `Error verification unauthorized, the did provided has not access`
	ERRORRevID            = `Error revocation unauthorized, the did provided has not access`
	ERRORVerSign          = `Error verifying signature`
	ERRORRevSign          = `Error revoking signature`
	ERRORRevoke           = `Error revoking Unauthorized, the did provided cannot revoke the identity`
	ERRORnotID            = `Error the identity does not exist`
	ERRORParsingID        = `Error parsing identity`
	ERRORRevokeLedger     = `Error deleting from ledger`
	ERRORIDExists         = `Error the identity already exists`
	ERRORUserAccess       = `Error user has not access`
	ERRORParseJWS         = `Error parsing into JWS`
	ERRORParseX509        = `Error parsing into X509`
	ERRORBase64           = `Error decoding into base64`
	ERRORVerifying        = `Error verifying signature `
	IDGATEWAY             = `ID Gateway`
	IDREGISTRY            = `ID Registry`
	ISSUERREGISTRY		  = `ISSUER Registry`
	ENTITYREGISTRY		  = `ENTITY Registry`
	ServiceGATEWAY        = `ID Service Gateway`
	ServiceREGISTRY       = `ID Service Registry`
	JOSEUTIL              = `JOSE Util`
	EDSA				  =	`EDSA`
)