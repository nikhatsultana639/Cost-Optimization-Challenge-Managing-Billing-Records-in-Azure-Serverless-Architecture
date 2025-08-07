# 📄 Cold Data Archival Strategy: Azure Cosmos DB to Azure Blob Storage (Cool Tier)

## 📌 Objective

To reduce storage costs by migrating **billing records older than 3 months** from **Azure Cosmos DB** to **Azure Blob Storage (Cool Tier)**, ensuring:

- ✅ No data loss
- ✅ Seamless access to historical data
- ✅ No changes to existing API contracts
- ✅ Minimal ongoing maintenance

---

## 🧱 Architecture Overview

This solution uses a **tiered storage** model:

| Tier        | Storage Type                  | Data Range                  |
|-------------|-------------------------------|-----------------------------|
| **Hot Tier**  | Azure Cosmos DB               | Recent records (≤ 3 months) |
| **Cold Tier** | Azure Blob Storage (Cool Tier) | Archived records (> 3 months) |

---

## 🛠️ Migration Strategy

### ✅ Phase 1: One-Time Historical Data Migration

#### Tool
- **Azure Cosmos DB Data Migration Tool (Desktop)**

#### Purpose
Export existing records older than 3 months and upload them to Azure Blob Storage.

#### Steps

1. **Install Tool**
   - [Download the Data Migration Tool](https://learn.microsoft.com/en-us/azure/cosmos-db/import-data)

2. **Configure Export**
   - Connect to your Cosmos DB instance
   - Use a custom SQL query:
     ```sql
     SELECT * FROM c WHERE c.timestamp < "<3-month-old-date>"
     ```

3. **Export to JSON Files**
   - Choose **JSON** as output format.

4. **Upload to Azure Blob Storage**
   - Use Azure Storage Explorer or AzCopy:
     ```bash
     azcopy copy "./data/*.json" "https://<account>.blob.core.windows.net/<container>?<SAS>" --blob-tier Cool
     ```

---

### ✅ Phase 2: Ongoing Cold Data Migration (Automated)

You can automate ongoing archival using **Azure Function App** or **Azure Data Factory (ADF)**.

---

## Option A: 🚀 Azure Function App (Timer-Triggered)

> Use this approach if you prefer a **lightweight, code-first, serverless solution**.

### 📁 Relevant Files

- `host.json`
- `function_app/init.py`

### Features

- Runs daily/weekly via timer trigger
- Filters records older than 3 months
- Uploads JSON to Blob Storage with `Cool` tier
- (Optional) Deletes archived records from Cosmos DB

---

## Option B: 🔄 Azure Data Factory (If Microsoft Fabric License Available)

> Ideal for teams already using **Azure Data Factory or Microsoft Fabric**.

### Features

- Low-code UI for managing pipelines
- Cosmos DB as source with timestamp filter
- Blob Storage (Cool tier) as sink
- Schedule with ADF triggers

---

## ✅ Unified Data Access Layer

Your existing API can read from both hot and cold tiers seamlessly:

1. Attempt to read from **Cosmos DB**
2. If not found, fallback to **Blob Storage**
3. Return the result to the client

📁 Reference File:  
- `get_record.py`

---

## 🔐 Security & Best Practices

- Use **Managed Identity** to access Cosmos DB and Blob securely
- Enable **Soft Delete** and **Versioning** on Blob Storage
- Apply **RBAC** to control data access
- Monitor with **Azure Monitor** and **Application Insights**

---

## 💰 Business Value

| Benefit               | Description                                                  |
|------------------------|--------------------------------------------------------------|
| **Cost Optimization**  | Blob Cool tier is 50–70% cheaper than Cosmos DB for archive  |
| **Retention Compliance** | Maintain historical records for audits                     |
| **Performance**        | Cold data accessible within seconds                          |
| **No API Changes**     | Existing clients keep using the same APIs                    |

---

## 📦 Deployment Reference

📁 **Blob Storage Deployment Script**  
- `blob_storage.bicep`

```bicep
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'mycoolstorage${uniqueString(resourceGroup().id)}'
  location: resourceGroup().location
  sku: {
    name: 'Standard_GRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Cool'
  }
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storage.name}/default/my-cool-container'
  properties: {
    publicAccess: 'None'
  }
}
