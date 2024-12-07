using '../main.bicep'

param location = 'North Europe'
param appServicePlanName = 'npchain-asp'
param keyVaultName = 'npchain-kv'
param registryName = 'NPChainACR'
param webappName = 'npchain-webapp'
param roleAssignments = [{
  principalId: '25d8d697-c4a2-479f-96e0-15593a830ae5'
  roleDefinitionIdOrName: 'Key Vault Secrets User'
  principalType: 'ServicePrincipal'
}]


