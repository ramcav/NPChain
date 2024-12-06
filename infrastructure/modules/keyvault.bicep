@description('Name of the Azure Key Vault')
param keyVaultName string

@description('Location of the Azure Key Vault')
param location string = resourceGroup().location


@description('Specifies if the vault is enabled for deployment by script or compute.')
param enableVaultForDeployment bool = true

@description('Enable RBAC for the Key Vault')
param enableRbac bool = true

@description('Specifies the SKU for the vault.')
param sku string = 'standard'

@description('Role assignment for the Key Vault')
param roleAssignments array

var builtInRoleNames = {
  'Key Vault Secrets User': subscriptionResourceId(
    'Microsoft.Authorization/roleDefinitions',
    '4633458b-17de-408a-b874-0445c86b69e6'
  )
}

// Key Vault Resource
resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    enabledForDeployment: enableVaultForDeployment
    enableRbacAuthorization: enableRbac
    
    sku: {
      name: sku
      family: 'A'
    }
    accessPolicies: [ ]
    tenantId: subscription().tenantId
  }
}

// Role Assignment
resource kv_roleAssignments 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for (roleAssignment, index) in (roleAssignments ?? []): {
    name: guid(keyVault.id, roleAssignment.principalId, roleAssignment.roleDefinitionIdOrName)
    properties: {
      roleDefinitionId: builtInRoleNames[?roleAssignment.roleDefinitionIdOrName] ?? roleAssignment.roleDefinitionIdOrName
      principalId: roleAssignment.principalId
    }
    scope: keyVault
  }
]
// Outputs
@description('The resource ID of the key vault.')
output resourceId string = keyVault.id

@description('The URI of the key vault.')
output keyVaultUri string = keyVault.properties.vaultUri
