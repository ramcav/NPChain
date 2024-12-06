@description('Name of the Azure Key Vault')
param keyVaultName string

@description('Location of the Azure Key Vault')
param location string = resourceGroup().location


@description('Specifies if the vault is enabled for deployment by script or compute.')
param enableVaultForDeployment bool = true


@description('Specifies the SKU for the vault.')
param sku string = 'standard'

@description('Role assignment for the Key Vault')
param roleAssignment object = {
  principalId: '7200f83e-ec45-4915-8c52-fb94147cfe5a'
  roleDefinitionIdOrName: 'Key Vault Secrets User'
  principalType: 'ServicePrincipal'
}

// Key Vault Resource
resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    enabledForDeployment: enableVaultForDeployment
    
    sku: {
      name: sku
      family: 'A'
    }
    accessPolicies: [ ]
    tenantId: subscription().tenantId
  }
}

// Role Assignment
resource kv_roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().subscriptionId, keyVaultName, roleAssignment.principalId)
  scope: keyVault
  properties: {
    principalId: roleAssignment.principalId
    roleDefinitionId: roleAssignment.roleDefinitionIdOrName
    principalType: roleAssignment.principalType
  }
}

// Outputs
@description('The resource ID of the key vault.')
output resourceId string = keyVault.id

@description('The URI of the key vault.')
output keyVaultUri string = keyVault.properties.vaultUri
