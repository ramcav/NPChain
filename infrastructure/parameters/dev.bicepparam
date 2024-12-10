using '../main.bicep'

param location = 'North Europe'
param appServicePlanName = 'npchain-asp'
param keyVaultName = 'npchain-kv'
param registryName = 'NPChainACR'
param webappName = 'npchain-webapp'
param roleAssignments = [
  {
    principalId: '25d8d697-c4a2-479f-96e0-15593a830ae5' // BCSAI2024-DEVOPS-STUDENTS-A-SP
    roleDefinitionIdOrName: 'Key Vault Secrets User'
    principalType: 'ServicePrincipal'
    }
    {
      principalId: 'a03130df-486f-46ea-9d5c-70522fe056de' // BCSAI2024-DEVOPS-STUDENTS-A
      roleDefinitionIdOrName: 'Key Vault Administrator'
      principalType: 'Group'
      }
]




