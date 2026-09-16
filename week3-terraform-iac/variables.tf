variable "aws_region" {
  type        = string
  description = "Target deployment region"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Deployment lifecycle stage"
  default     = "production"
}

variable "vpc_cidr" {
  type        = string
  description = "Base CIDR block for the Virtual Private Cloud"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  type        = string
  description = "CIDR block for public tier (Load Balancer / Ingress)"
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  type        = string
  description = "CIDR block for private tier (Application Pods / Database)"
  default     = "10.0.2.0/24"
}