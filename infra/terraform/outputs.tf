output "resource_group_name" {
  value = azurerm_resource_group.ops.name
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.ops.id
}

output "application_insights_name" {
  value = azurerm_application_insights.ops.name
}

output "automation_account_name" {
  value = azurerm_automation_account.ops.name
}

output "action_group_id" {
  value = azurerm_monitor_action_group.ops.id
}
