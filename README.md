# Secure CIE Authentication Protocol

This repository contains the design, theoretical security analysis, and partial Python implementation of a secure authentication protocol based on the Italian Electronic Identity Card (CIE). The project aims to provide a robust system for digital credential issuance and verification, balancing confidentiality, integrity, transparency, and efficiency.

## 📖 Overview and Threat Model

The system defines interactions between honest actors (Users, Authorities, Service Servers, Ufficio Anagrafe, and IPZS) and evaluates defenses against a comprehensive threat model. The protocol is designed to withstand various adversarial attacks, including:
* **Passive Eavesdropping** (Bob) and **Active Impersonation** (Alice).
* **Man-in-the-Middle Attacks** (George) attempting to manipulate credential requests.
* **Rogue Servers** (Jack) attempting to steal user information during the service access phase.
* **Denial of Service** (The Trickster's crew) targeting the availability of the infrastructure.

## 🧠 Cryptographic Architecture

The proposed solution ensures secure identification and credential management through advanced cryptographic primitives:

* **CIE Interaction (ECDSA):** Users securely communicate with their CIE via a TLS connection. After successful PIN validation, the CIE generates an ECDSA digital signature to authenticate the user to the issuing Authority.
* **Credential Generation (Merkle Trees):** The Authority constructs a Merkle Tree combining the user's public key ($pk_u$) and the credential metadata using SHA256. The Authority then signs the root of the Merkle Tree, ensuring the credential's integrity and authenticity.
* **Zero-Knowledge Authentication (Schnorr Protocol):** To access a qualified service, users provide their public key, the credential, and the Merkle proof. They prove ownership of the credential without revealing their private key ($sk_u$) by successfully completing the Schnorr identification protocol (a Zero-Knowledge Proof).

## 💻 Python Implementation

A proof-of-concept is implemented in Python using an Object-Oriented Programming (OOP) approach to emulate the network interactions between different machines. Core components include:

* `User`: Manages user data and establishes secure connections with server.
* `Server`: Base class extended by `ServerAuthority` (handles credential issuance) and `ServerService` (handles service access requests).
* `MerkleTree`: Implements a binary hash tree managing leaves, internal nodes, and the root using the SHA256 cryptographic hash function.
* `CIE`: Simulates the smart card behavior, exposing a `sign` method that utilizes OpenSSL to sign data only if the correct PIN is provided.

## 🔐 Security Analysis

The protocol guarantees:
* **Confidentiality:** Data privacy is maintained via TLS channels, and private keys remain strictly anonymous thanks to the Zero-Knowledge proofs.
* **Integrity:** Digital signatures and Merkle Trees prevent unauthorized data alteration, while the Schnorr protocol binds the credential to its legitimate owner.
* **Transparency:** The system avoids obscure third-party dependencies, relying entirely on publicly known, standardized cryptographic algorithms (ECDSA, Schnorr, SHA256).
