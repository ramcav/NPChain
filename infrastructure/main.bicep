@description('The Azure location where the resources will be deployed')
param location string = resourceGroup().location

// Key Vault Module Variables
@description('Name of the Azure Key Vault')
param keyVaultName string

// ACR Module Variables
@description('Name of the Azure Container Registry')
param registryName string
@description('SKU for the Azure Container Registry')
param sku string = 'Standard'

// App Service Plan Module Variables
@description('Name of the Azure App Service Plan')
param appServicePlanName string

// Webapp Module Variables
@description('Name of the Azure Webapp for Linux Container')
param webappName string
@description('Container Registry Image Name for the Azure Webapp for Linux Container')
param containerRegistryImageName string = 'npchain'
@description('Container Registry Image Version for the Azure Webapp for Linux Container')
param containerRegistryImageVersion string = 'latest'
@description('Dcoker Registry Server Username for the Azure Webapp for Linux Container')
var dockerRegistryServerUsername = 'acrAdminUsername'
@description('Dcoker Registry Server Password for the Azure Webapp for Linux Container')
var dockerRegistryServerPassword = 'acrAdminPassword0'

// Key Vault Module
module keyvault './modules/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    keyVaultName: keyVaultName
    location: location
  }
}

// ACR Module
module acr './modules/acr.bicep' = {
  name: 'acr'
  params: {
    registryName: registryName
    location: location
    sku: sku
    keyVaultResourceId: keyvault.outputs.resourceId
    keyVaultSecretNameAdminUsername: 'acrAdminUsername'
    keyVaultSecretNameAdminPassword0: 'acrAdminPassword0'
    keyVaultSecretNameAdminPassword1: 'acrAdminPassword1'
  }
  dependsOn: [
    keyvault
  ]
}

// App Service Plan Module
module appServicePlan './modules/asp.bicep' = {
  name: 'appServicePlan'
  params: {
    appServicePlanName: appServicePlanName
    location: location
  }
}

// KeyVault Reference
resource keyVaultReference 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
 }

// Webapp Module

module webapp './modules/webapp.bicep' = {
  name: 'webapp'
  params: {
    webappName: webappName
    location: location
    appServicePlanId: appServicePlan.outputs.appServicePlanId
    containerRegistryName: acr.outputs.registryLoginServer
    containerRegistryImageName: containerRegistryImageName
    containerRegistryImageVersion: containerRegistryImageVersion
    dockerRegistryServerUrl: acr.outputs.registryLoginServer
    dockerRegistryServerUsername: keyVaultReference.getSecret(dockerRegistryServerUsername)
    dockerRegistryServerPassword: keyVaultReference.getSecret(dockerRegistryServerPassword)
  }
}

