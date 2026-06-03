variable "location" {
  description = "Azure region for the MSP operations center."
  type        = string
  default     = "koreacentral"
}

variable "prefix" {
  description = "Short naming prefix."
  type        = string
  default     = "mspops"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "alert_email" {
  description = "Email address for Azure Monitor action group notifications."
  type        = string
  default     = "cloud-ops@example.com"
}

variable "customers" {
  description = "Customer names represented in workbook parameters and tags."
  type        = list(string)
  default     = ["contoso-retail", "fabrikam-clinic", "northwind-campus"]
}

variable "required_tags" {
  description = "Required tags for MSP-managed resources."
  type        = map(string)
  default = {
    owner       = "cloud-ops"
    environment = "dev"
    costCenter  = "msp-demo"
    customer    = "msp-operations"
  }
}

variable "enable_alert_rules" {
  description = "Create scheduled query alert rules after required Log Analytics tables exist."
  type        = bool
  default     = false
}
