# 1. Virtual Private Cloud Boundary
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# 2. Public Subnet (DMZ Tier)
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"

  tags = {
    Name        = "${var.environment}-public-subnet"
    Tier        = "Public"
    ManagedBy   = "Terraform"
  }
}

# 3. Private Subnet (Application & Compute Tier)
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = "${var.aws_region}a"

  tags = {
    Name        = "${var.environment}-private-subnet"
    Tier        = "Private"
    ManagedBy   = "Terraform"
  }
}

# 4. Internet Gateway (Inbound/Outbound routing for public tier)
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name      = "${var.environment}-igw"
    ManagedBy = "Terraform"
  }
}

# 5. Public Route Table (Routes 0.0.0.0/0 to the Internet Gateway)
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name      = "${var.environment}-public-rt"
    ManagedBy = "Terraform"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}

# 6. SRE Application Security Group (Firewall Rules)
resource "aws_security_group" "app_sg" {
  name        = "${var.environment}-app-security-group"
  description = "Ingress rules for HTTPS, HTTP, and internal health checks"
  vpc_id      = aws_vpc.main.id

  # Inbound HTTPS
  ingress {
    description = "Allow inbound HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound HTTP
  ingress {
    description = "Allow inbound HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound All Traffic (for updates and outbound API calls)
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "${var.environment}-app-sg"
    ManagedBy = "Terraform"
  }
}