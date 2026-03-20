# fin-secure-access-showcase
A technical showcase of an AI-driven web banking security prototype.

# Fin Secure Access: AI-Driven Banking Security & Fraud Detection System

> **⚠️ Important Notice Regarding Source Code**
> The full source code for this project is currently private and held under copyright by the Asia Pacific University of Technology and Innovation (APU) as part of a Final Year Project submission. 
> 
> This repository serves as a technical showcase of the system's architecture, machine learning models, and user interface.

![System Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Machine Learning](https://img.shields.io/badge/AI-Random_Forest_%7C_XGBoost-orange)
![Security](https://img.shields.io/badge/Security-WAF_%7C_MFA_%7C_PCI--DSS-red)

## 📌 Project Overview
**Fin Secure Access** is a next-generation web banking prototype designed to mitigate sophisticated financial crimes. It moves beyond static rule-based checks by integrating a **hybrid security architecture** that combines traditional security layers with real-time Machine Learning anomaly detection.

## 🚀 Key Features & Implementation
* **Real-Time AI Fraud Detection:** Utilized **Scikit-Learn (Random Forest and XGBoost)** to process transaction telemetry and output real-time confidence scores.
* **Web Application Firewall (WAF):** Engineered custom middleware in Python to intercept and neutralize malicious payloads.
* **Multi-Factor Authentication (MFA):** Integrated Time-based One-Time Passwords (TOTP) via Google Authenticator.

## ⚙️ System Architecture (Three-Tier)
The system was built using an Agile methodology and operates on a strict 3-tier architecture to ensure separation of concerns and maximum security.

![System Architecture](architecture-diagram.png) 

## 📸 System Previews

### Secure User Authentication
![MFA Login](mfa-login-screenshot.png)
*Secure login portal enforcing strict access control via TOTP.*
