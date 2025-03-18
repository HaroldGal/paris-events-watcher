### ⚙️ **Setup Instructions**

#### **1️⃣ Create a Custom Source**
1. Go to **Sources** in Airbyte UI.  
2. Select **"Custom Connector"**.  
3. Copy and paste the **custom source configuration** (`paris-open-data.yaml`).  
4. Save and **test the connection**.  

#### **2️⃣ Create a New Connection**
1. Go to **Connections** in Airbyte UI.  
2. Click **"New Connection"**.  
3. Select:  
   - **Source:** `Paris Open Data`  
   - **Destination:** Your data warehouse (e.g., BigQuery)  
4. Configure manual sync because it will be triggered by airflow.
5. Save the connection.

#### **3 Authentification from airflow**
1. Use conenctionId of your created conenction to link your airflow step
2. Update your airflow Admin connection with your credentials of airbyte (in settings.Application)
