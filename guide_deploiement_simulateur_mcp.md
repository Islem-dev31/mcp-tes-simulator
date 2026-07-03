# Guide de Déploiement Gratuit : Simulateur MCP TES

Ce guide explique étape par étape comment déployer gratuitement votre application Streamlit de simulation industrielle de batterie thermique (MCP TES) afin que le jury du **Greentech Challenge** puisse y accéder directement en ligne depuis un navigateur (PC, tablette ou smartphone).

---

## La Solution de Déploiement : Streamlit Community Cloud

La méthode la plus simple, rapide et entièrement gratuite pour déployer une application Streamlit est d'utiliser **Streamlit Community Cloud**. 
* **Coût** : 0 DA (Gratuit à vie pour les projets open-source/publics).
* **Temps de déploiement** : Moins de 5 minutes.
* **Mises à jour** : Automatiques (chaque fois que vous mettez à jour votre code sur GitHub, l'application en ligne se met à jour toute seule).

---

## Étape 1 : Préparation du Projet Local

Avant de publier l'application, nous devons vérifier que tous les fichiers nécessaires sont présents dans votre dossier de travail `C:\Users\AURES\Desktop\MCP`.

Votre dossier doit contenir au minimum les 3 fichiers suivants :
1. **`app.py`** : Le code principal de l'interface utilisateur Streamlit.
2. **`config.py`** : La base de données climatique et physique du projet.
3. **`requirements.txt`** : La liste des dépendances Python requises.

### Contenu du fichier `requirements.txt`
Assurez-vous que votre fichier `requirements.txt` contient exactement les lignes suivantes :
```text
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
openpyxl>=3.1.0
```

---

## Étape 2 : Publication sur GitHub

Streamlit Community Cloud déploie les applications directement depuis un dépôt GitHub. Vous devez donc y héberger votre code.

1. **Créer un compte GitHub** : Si ce n'est pas déjà fait, créez un compte gratuit sur [github.com](https://github.com/).
2. **Créer un nouveau dépôt (Repository)** :
   * Cliquez sur **New** ou allez sur [github.com/new](https://github.com/new).
   * Nommez le dépôt : `mcp-tes-simulator`.
   * Laissez le dépôt en **Public** (obligatoire pour le niveau gratuit de Streamlit Cloud).
   * Ne cochez pas "Add a README file" ou "Add .gitignore".
   * Cliquez sur **Create repository**.

3. **Pousser votre code local vers GitHub** :
   Ouvrez PowerShell dans votre dossier `C:\Users\AURES\Desktop\MCP` et exécutez les commandes suivantes :
   ```bash
   # Associer votre dépôt distant GitHub (remplacez par votre propre URL)
   git remote add origin https://github.com/VOTRE_NOM_UTILISATEUR/mcp-tes-simulator.git
   
   # Renommer la branche par défaut en main
   git branch -M main
   
   # Envoyer le code sur GitHub
   git push -u origin main
   ```
   *(Si Windows vous demande de vous connecter à GitHub, validez l'authentification dans votre navigateur).*

---

## Étape 3 : Déploiement sur Streamlit Cloud

1. Rendez-vous sur [share.streamlit.io](https://share.streamlit.io/).
2. Cliquez sur **Connect with GitHub** et connectez-vous avec vos identifiants GitHub.
3. Une fois connecté à votre tableau de bord Streamlit, cliquez sur le bouton **New app** (en haut à droite).
4. Remplissez le formulaire de déploiement :
   * **Repository** : Sélectionnez ou collez `VOTRE_NOM_UTILISATEUR/mcp-tes-simulator`.
   * **Branch** : Laissez `main`.
   * **Main file path** : Saisissez `app.py`.
   * **App URL** (Optionnel) : Vous pouvez personnaliser l'adresse Web (ex: `mcp-tes-simulation`).
5. Cliquez sur **Deploy!**.

L'application va commencer son processus d'installation. Streamlit va créer un conteneur virtuel, installer Python, lire votre fichier `requirements.txt` pour installer les dépendances (pandas, numpy, plotly, etc.), puis démarrer l'application. Cette étape prend entre 1 et 2 minutes lors du premier déploiement.

---

## Étape 4 : Partage et Utilisation

Une fois le déploiement terminé, votre application s'ouvre automatiquement dans votre navigateur.
* **URL de l'application** : Elle ressemblera à `https://mcp-tes-simulator.streamlit.app/`.
* **Partage** : Vous pouvez copier cette adresse et l'envoyer au jury, l'intégrer dans votre présentation de soutenance ou la partager sur vos supports de communication.
* **Mise à jour** : Si vous modifiez `app.py` ou `config.py` localement, il vous suffit de faire :
  ```bash
  git add .
  git commit -m "Mise à jour des paramètres"
  git push origin main
  ```
  L'application en ligne se rechargera automatiquement avec vos modifications en quelques secondes !
