using '../main.bicep'

param location = 'North Europe'
param appServicePlanName = 'npchain-asp'
param keyVaultName = 'npchain-kv'
param registryName = 'NPChainACR'
param webappName = 'npchain-webapp'
param roleAssignments = [{
  principalId: '797f4846-ba00-4fd7-ba43-dac1f8f63013'
  roleDefinitionIdOrName: 'Key Vault Secrets User'
  principalType: 'ServicePrincipal'
}]


