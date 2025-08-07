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
