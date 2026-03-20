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

![System Architecture](https://github.com/Julio0702/fin-secure-access-showcase/blob/e87de52b812144f6449c4536b74219c981be6132/image.png) 

## 📸 System Previews


### 1. Real-Time Fraud Interception
![Fraud Alert](https://github.com/Julio0702/fin-secure-access-showcase/blob/5e56257273ea81539b8896db700c4e58a2ab73fe/fraud%20alert.png)
*The AI engine successfully identifies a high-value anomaly and triggers an immediate block, providing Explainable AI (XAI) feedback to the user.*

### 2. Secure User Dashboard
![Dashboard](https://github.com/Julio0702/fin-secure-access-showcase/blob/17345b8176b8c906e03060b8ff5513473cc5d6b0/Dailylimit.png)
*The main interface featuring a live activity feed and user-defined risk controls (Daily Transfer Limits).*

### 3. Multi-Factor Authentication
![MFA Setup](https://github.com/Julio0702/fin-secure-access-showcase/blob/17345b8176b8c906e03060b8ff5513473cc5d6b0/Setup-2FA.png)

![MFA Login](https://github.com/Julio0702/fin-secure-access-showcase/blob/17345b8176b8c906e03060b8ff5513473cc5d6b0/2FA.png)

*Secure login portal enforcing strict access control via TOTP.*

### 4. Web Application Firewall (WAF) Interception
![WAF Block](https://github.com/Julio0702/fin-secure-access-showcase/blob/17345b8176b8c906e03060b8ff5513473cc5d6b0/WAFblock.png)
*Custom middleware successfully detecting and neutralizing a malicious payload (e.g., SQL Injection) before it can reach the backend application layer.*
