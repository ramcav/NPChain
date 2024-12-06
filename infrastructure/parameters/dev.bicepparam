using '../main.bicep'

param location = 'North Europe'
param appServicePlanName = 'npchain-asp'
param keyVaultName = 'npchain-kv'
param registryName = 'NPChainACR'
param webappName = 'npchain-webapp'
param roleAssignments = [{
  principalId: '7200f83e-ec45-4915-8c52-fb94147cfe5a'
  roleDefinitionIdOrName: 'Key Vault Secrets User'
  principalType: 'ServicePrincipal'
}]


