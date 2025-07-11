# WayTrek API

A FastAPI-based travel and trip management API deployed as AWS Lambda with SAM (Serverless Application Model).

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **AWS Lambda**: Serverless compute with automatic scaling
- **AWS SAM**: Infrastructure as Code with simplified templates
- **API Gateway**: RESTful API with custom domain support
- **PostgreSQL**: RDS database with Alembic migrations
- **AWS Cognito**: Authentication and user management
- **S3**: File storage
- **Auto-scaling**: Pay-per-request serverless scaling
- **CI/CD**: GitHub Actions with SAM CLI

## Architecture

- **AWS Lambda**: Serverless function running FastAPI application
- **API Gateway**: RESTful API with SSL termination and custom domain
- **RDS PostgreSQL**: Database in private subnets with VPC
- **ECR**: Container registry for Lambda container images
- **CloudWatch**: Automatic logging and monitoring
- **Route 53**: DNS management for custom domain
- **Cognito User Pool**: User authentication and management (auto-created)
- **S3 Bucket**: File storage with encryption and lifecycle policies (auto-created)

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS SAM CLI** installed locally for development
3. **Docker** installed for local testing
4. **Domain**: `api.waytrek.app` configured in your DNS
5. **SSL Certificate**: ACM certificate for your domain
6. **GitHub Secrets**: Required environment variables

## Required GitHub Secrets

Set these secrets in your GitHub repository:

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
DB_MASTER_PASSWORD=your_secure_database_password
```

**Note**: Cognito and S3 resources are now created automatically by the SAM template, so you no longer need to set those secrets manually!

## Deployment

### Automatic Deployment

The application automatically deploys when you push to the `main` branch:

1. **Tests**: Runs security scans and tests
2. **SAM Build**: Builds the serverless application
3. **SAM Deploy**: Deploys infrastructure (Lambda, API Gateway, Cognito, S3, RDS)
4. **Docker Build**: Builds and pushes container image to ECR
5. **Lambda Update**: Updates Lambda function with new image
6. **Migrate**: Runs database migrations
7. **Verify**: Confirms deployment success

**New Resources Created Automatically**:
- Cognito User Pool with secure password policies
- Cognito User Pool Client with OAuth2 configuration
- S3 Bucket with encryption and lifecycle policies
- All necessary IAM roles and policies

### Manual Deployment

If you need to deploy manually:

1. **Install SAM CLI**:
   ```bash
   # macOS
   brew install aws-sam-cli
   
   # Windows
   choco install aws-sam-cli
   
   # Linux
   pip install aws-sam-cli
   ```

2. **Configure AWS CLI**:
   ```bash
   aws configure
   ```

3. **Deploy with SAM**:
   ```bash
   # Build the application
   sam build --use-container
   
   # Deploy to AWS
   sam deploy --guided
   ```

4. **Quick Deploy (after first deployment)**:
   ```bash
   sam deploy
   ```

### Local Development with SAM

1. **Start API locally**:
   ```bash
   sam local start-api --port 8000
   ```

2. **Test specific function**:
   ```bash
   sam local invoke WayTrekFunction --event events/api_event.json
   ```

3. **Build and test**:
   ```bash
   sam build --use-container
   sam local start-api --port 8000 --host 0.0.0.0
   ```

## Traditional Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd waytrek-api
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the application**:
   ```bash
   # Traditional FastAPI development
   python main.py
   
   # OR with SAM for Lambda simulation
   sam local start-api --port 8000
   ```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: `https://api.waytrek.app/docs`
- **ReDoc**: `https://api.waytrek.app/redoc`
- **OpenAPI JSON**: `https://api.waytrek.app/api/v1/openapi.json`

## Project Structure

```
waytrek-api/
├── modules/                 # Feature modules
│   ├── activities/         # Activity management
│   ├── locations/          # Location management
│   ├── saved_list/         # Saved items
│   ├── trips/              # Trip management
│   └── users/              # User management
├── db/                     # Database configuration
├── migrations/             # Alembic migrations
├── utils/                  # Utility functions
├── .github/workflows/      # GitHub Actions
├── template.yaml           # CloudFormation template
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
├── main.py               # Application entry point
└── config.py             # Configuration settings
```

## Monitoring

- **CloudWatch Logs**: `/aws/lambda/waytrek-api-production-WayTrekFunction`
- **Lambda Console**: Monitor function performance and errors
- **API Gateway**: Request/response monitoring and metrics
- **RDS Monitoring**: Database performance metrics
- **X-Ray**: Distributed tracing (optional)

## Scaling

The serverless infrastructure automatically scales:

- **Lambda**: Scales from 0 to 15,000 concurrent executions
- **API Gateway**: Handles 10,000 requests per second by default
- **RDS**: Can scale compute and storage independently
- **Pay-per-use**: Only pay for actual requests and compute time

No manual scaling configuration required!

## Security

- **VPC**: Private subnets for database
- **Security Groups**: Restrictive ingress rules for RDS
- **IAM Roles**: Least privilege access for Lambda
- **SSL/TLS**: HTTPS only with ACM certificates
- **Container Security**: Non-root user in containers
- **API Gateway**: Built-in DDoS protection and throttling
- **Secrets**: Environment variables managed securely

## Troubleshooting

1. **Check Lambda Function Logs**:
   ```bash
   aws logs tail /aws/lambda/waytrek-api-production-WayTrekFunction --follow
   ```

2. **View SAM deployment logs**:
   ```bash
   sam logs -n WayTrekFunction --stack-name waytrek-api-production --tail
   ```

3. **Test Lambda function locally**:
   ```bash
   sam local invoke WayTrekFunction --event events/api_event.json
   ```

4. **Check API Gateway**:
   ```bash
   aws apigateway get-rest-apis --query 'items[?name==`waytrek-api-production`]'
   ```

5. **Database Connection**:
   - Verify security group rules
   - Check RDS endpoint in environment variables
   - Ensure database is in running state

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. 