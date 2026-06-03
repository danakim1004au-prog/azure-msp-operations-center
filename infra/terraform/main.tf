resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

locals {
  name_prefix = "${var.prefix}-${var.environment}-${random_string.suffix.result}"
  common_tags = merge(var.required_tags, {
    project = "azure-msp-operations-center"
  })
}

resource "azurerm_resource_group" "ops" {
  name     = "rg-${local.name_prefix}"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_log_analytics_workspace" "ops" {
  name                = "law-${local.name_prefix}"
  location            = azurerm_resource_group.ops.location
  resource_group_name = azurerm_resource_group.ops.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.common_tags
}

resource "azurerm_application_insights" "ops" {
  name                = "appi-${local.name_prefix}"
  location            = azurerm_resource_group.ops.location
  resource_group_name = azurerm_resource_group.ops.name
  workspace_id        = azurerm_log_analytics_workspace.ops.id
  application_type    = "web"
  tags                = local.common_tags
}

resource "azurerm_storage_account" "ops" {
  name                            = replace("st${var.prefix}${var.environment}${random_string.suffix.result}", "-", "")
  resource_group_name             = azurerm_resource_group.ops.name
  location                        = azurerm_resource_group.ops.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  tags                            = local.common_tags
}

resource "azurerm_storage_container" "incident_artifacts" {
  name                  = "incident-artifacts"
  storage_account_name  = azurerm_storage_account.ops.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "model_outputs" {
  name                  = "model-outputs"
  storage_account_name  = azurerm_storage_account.ops.name
  container_access_type = "private"
}

resource "azurerm_automation_account" "ops" {
  name                = "aa-${local.name_prefix}"
  location            = azurerm_resource_group.ops.location
  resource_group_name = azurerm_resource_group.ops.name
  sku_name            = "Basic"
  tags                = local.common_tags

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_monitor_action_group" "ops" {
  name                = "ag-${local.name_prefix}"
  resource_group_name = azurerm_resource_group.ops.name
  short_name          = "mspops"
  tags                = local.common_tags

  email_receiver {
    name                    = "cloud-ops-email"
    email_address           = var.alert_email
    use_common_alert_schema = true
  }
}

resource "azurerm_monitor_scheduled_query_rules_alert_v2" "appservice_5xx" {
  count                = var.enable_alert_rules ? 1 : 0
  name                 = "alert-appservice-5xx-spike"
  resource_group_name  = azurerm_resource_group.ops.name
  location             = azurerm_resource_group.ops.location
  scopes               = [azurerm_log_analytics_workspace.ops.id]
  description          = "Detects high App Service 5xx error rate by customer and app."
  severity             = 2
  evaluation_frequency = "PT5M"
  window_duration      = "PT15M"
  enabled              = true
  tags                 = local.common_tags

  criteria {
    query                   = file("${path.module}/../../kql/appservice/appservice_5xx_spike.kql")
    time_aggregation_method = "Count"
    threshold               = 0
    operator                = "GreaterThan"
    failing_periods {
      minimum_failing_periods_to_trigger_alert = 1
      number_of_evaluation_periods             = 1
    }
  }

  action {
    action_groups = [azurerm_monitor_action_group.ops.id]
  }
}

resource "azurerm_monitor_scheduled_query_rules_alert_v2" "vm_heartbeat" {
  count                = var.enable_alert_rules ? 1 : 0
  name                 = "alert-vm-heartbeat-missing"
  resource_group_name  = azurerm_resource_group.ops.name
  location             = azurerm_resource_group.ops.location
  scopes               = [azurerm_log_analytics_workspace.ops.id]
  description          = "Detects VMs that stopped sending heartbeat events."
  severity             = 2
  evaluation_frequency = "PT5M"
  window_duration      = "PT15M"
  enabled              = true
  tags                 = local.common_tags

  criteria {
    query                   = file("${path.module}/../../kql/vm/vm_heartbeat_missing.kql")
    time_aggregation_method = "Count"
    threshold               = 0
    operator                = "GreaterThan"
    failing_periods {
      minimum_failing_periods_to_trigger_alert = 1
      number_of_evaluation_periods             = 1
    }
  }

  action {
    action_groups = [azurerm_monitor_action_group.ops.id]
  }
}

resource "azurerm_resource_group_policy_assignment" "require_customer_tag" {
  name                 = "require-customer-tag"
  resource_group_id    = azurerm_resource_group.ops.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/871b6d14-10aa-478d-b590-94f262ecfa99"
  display_name         = "Require customer tag on MSP managed resources"
  description          = "Demo policy assignment requiring a customer tag. Replace policy ID if your tenant uses custom initiatives."

  parameters = jsonencode({
    tagName = {
      value = "customer"
    }
  })
}
