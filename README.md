# 📊 Data Pipeline - Paris Events

![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white) ![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white) ![Airbyte](https://img.shields.io/badge/Airbyte-6A36D8?style=for-the-badge&logo=airbyte&logoColor=white) ![Looker Studio](https://img.shields.io/badge/Looker%20Studio-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white) ![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)

## 📌 Description
This project builds a data pipeline to collect, transform, and visualize **Paris events** using **Airbyte, dbt, BigQuery, and Looker Studio**. The entire process is orchestrated via **Airflow** for automated updates.
**Public Dashboard Link**: [Looker Studio Dashboard](https://lookerstudio.google.com/s/owd516emkqk)

---

## 🏗️ **Pipeline Architecture**

1️⃣ **Data Ingestion**:
   - Source: **Paris OpenData API** ([opendata.paris.fr](https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/information/?disjunctive.access_type&disjunctive.price_type&disjunctive.deaf&disjunctive.blind&disjunctive.pmr&disjunctive.address_city&disjunctive.address_zipcode&disjunctive.address_name&disjunctive.tags&disjunctive.programs&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQ09VTlQiLCJ5QXhpcyI6InBtciIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6IiNGRkNEMDAifV0sInhBeGlzIjoidXBkYXRlZF9hdCIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6ImRheSIsInNvcnQiOiIiLCJjb25maWciOnsiZGF0YXNldCI6InF1ZS1mYWlyZS1hLXBhcmlzLSIsIm9wdGlvbnMiOnsiZGlzanVuY3RpdmUuYWNjZXNzX3R5cGUiOnRydWUsImRpc2p1bmN0aXZlLnByaWNlX3R5cGUiOnRydWUsImRpc2p1bmN0aXZlLmRlYWYiOnRydWUsImRpc2p1bmN0aXZlLmJsaW5kIjp0cnVlLCJkaXNqdW5jdGl2ZS5wbXIiOnRydWUsImRpc2p1bmN0aXZlLmFkZHJlc3NfY2l0eSI6dHJ1ZSwiZGlzanVuY3RpdmUuYWRkcmVzc196aXBjb2RlIjp0cnVlLCJkaXNqdW5jdGl2ZS5hZGRyZXNzX25hbWUiOnRydWUsImRpc2p1bmN0aXZlLnRhZ3MiOnRydWUsImRpc2p1bmN0aXZlLnByb2dyYW1zIjp0cnVlfX19XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&basemap=jawg.dark&location=3,27.12049,1.64636))
   - Tool: **Airbyte** (HTTP API custom connector)
   - Storage: **BigQuery (landing layer)**

2️⃣ **Data Transformation**:
   - Tool: **dbt (Data Build Tool)**
   - Casting and testing into **Bronze layer**
   - Cleaning and structuring into **Silver layer**
   - Building a **Gold layer** for analytical insights

3️⃣ **Automation & Orchestration**: # IN PROGRESS
   - Tool: **Apache Airflow**
   - Scheduled daily ingestion and transformation
   - Automated dbt execution post-ingestion

---

## 📂 **Repository Structure**
```
📂 project_root/
├── airbytes/       # in progress
├── airflow/        # in progress
├── models/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
├── README.md
```

---

## 🚀 **Installation & Deployment**
### **1️⃣ Prerequisites**
- Google Cloud Platform (**BigQuery**)
- **dbt** installed and configured for BigQuery
- **Looker Studio** for data visualization
- Install **[Docker](https://www.docker.com/get-started)**.
- Install **[Docker Compose](https://docs.docker.com/compose/install/)**.

#### **dbt: Run Transformations**
```bash
dbt run
```

#### Setting Up Apache Airflow with Docker

We use **Docker Compose** to deploy **Apache Airflow** for orchestrating our data pipeline.

##### 🔧 **Setup Instructions**
- Follow **[the official Airflow Docker tutorial](https://airflow.apache.org/docs/apache-airflow/2.1.1/start/docker.html)**.
- Use the start.sh file to launch docker easily

##### Access the Web UI at http://localhost:8080
- Username: airflow
- Password: airflow

#### Setting Up Airbyte with abctl

Follow the airbyte repository which includes a README.

#### Link Airbyte and Airflow

As Airbyte and Airflow are on 2 differents isolated dockers, we have to setup a network to let airflow trigger Airbyte.

```bash
docker network create myNetwork
docker network connect myNetwork airflow-airflow-webserver-1
docker network connect myNetwork airbyte-abctl-control-plane
```

Then you can create your connection in Administrator panel on airflow UI.

- connection Type: Airbyte
- host: http://airbyte-abctl-control-plane/api/public/v1/
- Client ID: Get in Airbyte.settings.application
- Client Secret: Get in Airbyte.settings.application


---

## 🛠 **Author & Contact**
👤 **Name**: Harold Gallice
📧 **Contact**: haroldgallice@gmail.com  
💼 **LinkedIn**: [Harold](https://www.linkedin.com/in/harold-gallice-43656212a/)

🚀 **Happy Data Engineering!**
